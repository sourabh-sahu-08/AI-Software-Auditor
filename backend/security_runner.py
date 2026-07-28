import subprocess
import json
import os
import time

def run_security(project_path: str) -> dict:
    """
    Executes Bandit/Safety (Python) or npm audit (Node).
    Parses the JSON output to extract severity counts.
    """
    start_time = time.time()
    result = {
        "status": "FAIL",
        "high": 0,
        "medium": 0,
        "low": 0,
        "execution_time": 0.0,
        "output": ""
    }
    
    try:
        package_json_path = os.path.join(project_path, "package.json")
        output_str = ""
        process = None

        if os.path.exists(package_json_path):
            # Node.js - npm audit
            cmd = ["npm.cmd", "audit", "--json"] if os.name == 'nt' else ["npm", "audit", "--json"]
            process = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True, timeout=300)
            output_str = process.stdout
            try:
                data = json.loads(output_str)
                metadata = data.get("metadata", {}).get("vulnerabilities", {})
                result["high"] = metadata.get("high", 0) + metadata.get("critical", 0)
                result["medium"] = metadata.get("moderate", 0)
                result["low"] = metadata.get("low", 0)
                if result["high"] == 0 and result["medium"] == 0: result["status"] = "PASS"
                result["output"] = json.dumps(data, indent=2)
            except json.JSONDecodeError:
                result["output"] = output_str + "\n" + process.stderr
                if process.returncode == 0: result["status"] = "PASS"
        else:
            # Python - try bandit, fallback to safety
            try:
                process = subprocess.run(["bandit", "-r", ".", "-f", "json"], cwd=project_path, capture_output=True, text=True, timeout=300)
                output_str = process.stdout
                data = json.loads(output_str)
                metrics = data.get("metrics", {}).get("_totals", {})
                result["high"] = metrics.get("SEVERITY.HIGH", 0)
                result["medium"] = metrics.get("SEVERITY.MEDIUM", 0)
                result["low"] = metrics.get("SEVERITY.LOW", 0)
                if result["high"] == 0 and result["medium"] == 0: result["status"] = "PASS"
                result["output"] = json.dumps(data.get("results", []), indent=2)
            except (json.JSONDecodeError, FileNotFoundError):
                # Fallback to safety
                try:
                    process = subprocess.run(["safety", "check", "--json"], cwd=project_path, capture_output=True, text=True, timeout=300)
                    output_str = process.stdout
                    data = json.loads(output_str)
                    
                    if isinstance(data, dict):
                        vulns = data.get("vulnerabilities", [])
                    else:
                        vulns = data  # older versions returned a list directly
                        
                    result["high"] = len(vulns)  # Safety doesn't easily split by severity, count all as high
                    if result["high"] == 0: result["status"] = "PASS"
                    result["output"] = json.dumps(data, indent=2)
                except FileNotFoundError:
                    result["output"] = "Neither Bandit nor Safety found."

    except subprocess.TimeoutExpired as e:
        result["output"] = f"Security scan timed out after 5 minutes: {str(e)}"
    except Exception as e:
        result["output"] = f"An unexpected error occurred: {str(e)}"
        
    end_time = time.time()
    result["execution_time"] = round(end_time - start_time, 2)
    return result
