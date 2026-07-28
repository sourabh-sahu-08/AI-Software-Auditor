import subprocess
import re
import os
import time

def run_tests(project_path: str) -> dict:
    """
    Executes tests using pytest, unittest, or npm test.
    Parses the output to extract passed/failed counts.
    """
    start_time = time.time()
    result = {
        "status": "FAIL",
        "tests_passed": 0,
        "tests_failed": 0,
        "execution_time": 0.0,
        "output": ""
    }
    
    try:
        package_json_path = os.path.join(project_path, "package.json")
        output = ""
        process = None

        if os.path.exists(package_json_path):
            cmd = ["npm.cmd", "test"] if os.name == 'nt' else ["npm", "test"]
            process = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True, timeout=300)
            output = process.stdout + "\n" + process.stderr
            
            # Simple heuristic for mocha/jest etc
            passed_match = re.search(r'(\d+)\s+(?:passing|passed)', output, re.IGNORECASE)
            failed_match = re.search(r'(\d+)\s+failing', output, re.IGNORECASE)
            if passed_match: result["tests_passed"] = int(passed_match.group(1))
            if failed_match: result["tests_failed"] = int(failed_match.group(1))
        
        else:
            # Python - Try pytest first
            try:
                process = subprocess.run(["pytest"], cwd=project_path, capture_output=True, text=True, timeout=300)
                output = process.stdout + "\n" + process.stderr
                passed_match = re.search(r'(\d+)\s+passed', output)
                failed_match = re.search(r'(\d+)\s+failed', output)
                if passed_match: result["tests_passed"] = int(passed_match.group(1))
                if failed_match: result["tests_failed"] = int(failed_match.group(1))
                
                # If pytest says no tests found (code 5) or command not found, fallback to unittest
                if process.returncode == 5 or "no tests ran" in output.lower():
                    raise FileNotFoundError("Pytest found no tests, try unittest")
            except FileNotFoundError:
                process = subprocess.run(["python", "-m", "unittest", "discover"], cwd=project_path, capture_output=True, text=True, timeout=300)
                output = process.stdout + "\n" + process.stderr
                # Unittest output: "Ran 5 tests in 0.001s\n\nOK"
                ran_match = re.search(r'Ran (\d+) test', output)
                failures_match = re.search(r'failures=(\d+)', output)
                errors_match = re.search(r'errors=(\d+)', output)
                
                total = int(ran_match.group(1)) if ran_match else 0
                failed = (int(failures_match.group(1)) if failures_match else 0) + (int(errors_match.group(1)) if errors_match else 0)
                result["tests_passed"] = total - failed
                result["tests_failed"] = failed

        result["output"] = output
        if process and process.returncode == 0:
            result["status"] = "PASS"
            
    except subprocess.TimeoutExpired as e:
        result["output"] = f"Tests timed out after 5 minutes: {str(e)}"
    except Exception as e:
        result["output"] = f"An unexpected error occurred: {str(e)}"
        
    end_time = time.time()
    result["execution_time"] = round(end_time - start_time, 2)
    return result
