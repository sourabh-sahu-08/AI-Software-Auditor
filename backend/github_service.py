import requests
from typing import List, Dict, Any
import config

def fetch_open_issues(owner: str, repo: str) -> List[Dict[str, Any]]:
    """
    Fetches open issues for a given GitHub repository.
    Includes labels, author, and comment counts.
    """
    token = config.GITHUB_TOKEN
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    
    try:
        # We only want open issues, which is the default for the API
        params = {"state": "open", "per_page": 100}
        response = requests.get(url, headers=headers, params=params, timeout=config.REQUEST_TIMEOUT)
        
        # Handle specific HTTP status codes
        if response.status_code == 401:
            raise Exception("Invalid GitHub token. Please check your .env file or token validity.")
        elif response.status_code == 403:
            rate_limit_remaining = response.headers.get("X-RateLimit-Remaining")
            if rate_limit_remaining == "0":
                reset_time = response.headers.get("X-RateLimit-Reset", "unknown time")
                raise Exception(f"GitHub API rate limit exceeded. Resets at timestamp: {reset_time}")
            raise Exception("Access forbidden. Ensure your token has the correct permissions.")
        elif response.status_code == 404:
            raise Exception(f"Repository '{owner}/{repo}' not found or is private and requires a valid token.")
        
        response.raise_for_status()
        issues_data = response.json()
        
        formatted_issues = []
        for issue in issues_data:
            # GitHub API returns pull requests alongside issues in this endpoint; filter PRs out
            if "pull_request" in issue:
                continue
                
            labels = [label.get("name") for label in issue.get("labels", [])]
            formatted_issues.append({
                "Issue Number": issue.get("number"),
                "Title": issue.get("title"),
                "Body": issue.get("body") or "No description provided.",
                "State": issue.get("state"),
                "Created Date": issue.get("created_at"),
                "Updated Date": issue.get("updated_at"),
                "URL": issue.get("html_url"),
                "Labels": ", ".join(labels) if labels else "None",
                "Author": issue.get("user", {}).get("login", "Unknown"),
                "Comments": issue.get("comments", 0)
            })
            
        return formatted_issues
        
    except requests.exceptions.Timeout:
        raise Exception("Network timeout while trying to reach GitHub API. Please try again.")
    except requests.exceptions.ConnectionError:
        raise Exception("Network error. Please check your internet connection.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"An error occurred while fetching issues: {str(e)}")
