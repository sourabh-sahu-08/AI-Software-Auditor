import subprocess
import json
import os
import time

def run_lint(project_path: str) -> dict:
    """
    Executes pylint/flake8 (Python) or eslint (Node).
    Parses output to extract warnings and errors.
    """
    start_time = time.time()
    result = {
        "status": "FAIL",
        "warnings": 0,
        "errors": 0,
        "execution_time": 0.0,
        "output": ""
    }
    
    try:
        package_json_path = os.path.join(project_path, "package.json")
        output_str = ""
        process = None

        if os.path.exists(package_json_path):
            # Node.js - try eslint
            cmd = ["npx.cmd", "eslint", ".", "-f", "json"] if os.name == 'nt' else ["npx", "eslint", ".", "-f", "json"]
            process = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True, timeout=300)
            output_str = process.stdout
            try:
                issues = json.loads(output_str)
                for file_issues in issues:
                    result["warnings"] += file_issues.get("warningCount", 0)
                    result["errors"] += file_issues.get("errorCount", 0)
                if result["errors"] == 0: result["status"] = "PASS"
                result["output"] = json.dumps(issues, indent=2)
            except json.JSONDecodeError:
                result["output"] = output_str + "\n" + process.stderr
                if process.returncode == 0: result["status"] = "PASS"
        else:
            # Python - try pylint, fallback to flake8
            try:
                process = subprocess.run(["pylint", "--recursive=y", "--output-format=json", "."], cwd=project_path, capture_output=True, text=True, timeout=300)
                output_str = process.stdout
                
                if not output_str.strip() and process.returncode == 0:
                    result["status"] = "PASS"
                    result["output"] = "No linting issues found."
                else:
                    issues = json.loads(output_str)
                    for issue in issues:
                        type_name = issue.get("type", "").lower()
                        if type_name == "warning": result["warnings"] += 1
                        elif type_name in ["error", "fatal"]: result["errors"] += 1
                    if result["errors"] == 0: result["status"] = "PASS"
                    result["output"] = json.dumps(issues, indent=2)
            except (json.JSONDecodeError, FileNotFoundError):
                # Fallback to flake8
                try:
                    process = subprocess.run(["flake8", "."], cwd=project_path, capture_output=True, text=True, timeout=300)
                    output_str = process.stdout + "\n" + process.stderr
                    # Flake8 output is usually plain text. Every line is an issue.
                    lines = [line for line in output_str.split("\n") if line.strip()]
                    result["errors"] = len(lines)
                    if result["errors"] == 0: result["status"] = "PASS"
                    result["output"] = output_str if output_str.strip() else "No linting issues found."
                except FileNotFoundError:
                    result["output"] = "Neither pylint nor flake8 found."

    except subprocess.TimeoutExpired as e:
        result["output"] = f"Linting timed out after 5 minutes: {str(e)}"
    except Exception as e:
        result["output"] = f"An unexpected error occurred: {str(e)}"
        
    end_time = time.time()
    result["execution_time"] = round(end_time - start_time, 2)
    return result
