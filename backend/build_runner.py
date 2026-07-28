import os
import subprocess
import time

def run_build(project_path: str) -> dict:
    """
    Executes the appropriate build command for the project.
    If package.json exists, runs 'npm install' then 'npm run build'.
    Otherwise, runs 'python -m compileall .'
    """
    start_time = time.time()
    result = {
        "status": "FAIL",
        "output": "",
        "execution_time": 0.0
    }
    
    try:
        package_json_path = os.path.join(project_path, "package.json")
        
        if os.path.exists(package_json_path):
            # Install dependencies first
            install_cmd = ["npm.cmd", "install"] if os.name == 'nt' else ["npm", "install"]
            subprocess.run(
                install_cmd,
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=300
            )
            cmd = ["npm.cmd", "run", "build"] if os.name == 'nt' else ["npm", "run", "build"]
        else:
            cmd = ["python", "-m", "compileall", "."]
            
        process = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        end_time = time.time()
        result["execution_time"] = round(end_time - start_time, 2)
        result["output"] = process.stdout + "\n" + process.stderr
        
        if process.returncode == 0:
            result["status"] = "PASS"
            
    except subprocess.TimeoutExpired as e:
        end_time = time.time()
        result["execution_time"] = round(end_time - start_time, 2)
        result["output"] = f"Build timed out after 5 minutes: {str(e)}"
    except FileNotFoundError as e:
        end_time = time.time()
        result["execution_time"] = round(end_time - start_time, 2)
        result["output"] = f"Required build tool not found. Ensure npm/python is installed. Error: {str(e)}"
    except Exception as e:
        end_time = time.time()
        result["execution_time"] = round(end_time - start_time, 2)
        result["output"] = f"An unexpected error occurred: {str(e)}"
        
    return result
