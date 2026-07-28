import os
import json
from groq import Groq
import groq
from dotenv import load_dotenv
import config
load_dotenv()

def analyze_issue(issue_title: str, issue_description: str) -> dict:
    """
    Analyzes a GitHub issue using the Groq AI API.
    Returns a structured JSON containing root cause, suggested fix, etc.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise Exception("GROQ_API_KEY not found in .env file.")
        
    try:
        client = Groq(api_key=api_key)
        
        prompt = f"""
Analyze the following GitHub issue and provide ONLY a JSON object in this exact format:
{{
  "root_cause": "...",
  "suggested_fix": "...",
  "files_to_modify": ["..."],
  "confidence": 95,
  "claim": "Fixed"
}}

Do not include markdown blocks or any extra explanation outside of the JSON object. Ensure 'confidence' is an integer between 0 and 100, and 'files_to_modify' is a list of strings.

Issue Title: {issue_title}
Issue Description: {issue_description}
"""

        def attempt_analysis(model_name):
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=model_name,
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            
            parsed_json = json.loads(content)
            # Basic validation to ensure expected keys exist
            expected_keys = {"root_cause", "suggested_fix", "files_to_modify", "confidence", "claim"}
            if not expected_keys.issubset(parsed_json.keys()):
                raise Exception("JSON is missing required keys.")
            
            # Validate types
            if not isinstance(parsed_json.get("confidence"), int):
                try:
                    parsed_json["confidence"] = int(parsed_json["confidence"])
                except:
                    parsed_json["confidence"] = 0
                    
            if not isinstance(parsed_json.get("files_to_modify"), list):
                parsed_json["files_to_modify"] = [str(parsed_json["files_to_modify"])]
                
            return parsed_json

        # Try primary model first, with JSON retry logic
        def try_with_model(model_name):
            try:
                return attempt_analysis(model_name)
            except (json.JSONDecodeError, Exception) as first_err:
                if "JSON" in str(first_err) or "JSONDecodeError" in str(type(first_err)):
                    try:
                        return attempt_analysis(model_name)
                    except Exception as second_err:
                        raise Exception(f"Failed to generate valid JSON after 2 attempts with {model_name}. Last error: {second_err}")
                else:
                    raise first_err

        try:
            return try_with_model(config.GROQ_MODEL)
        except Exception as e:
            # If the error is not a JSON error, it might be a model decommission error or other API error
            # Attempt fallback model
            if "JSON" not in str(e):
                try:
                    return try_with_model(config.GROQ_FALLBACK_MODEL)
                except Exception as fallback_err:
                    raise Exception(f"Primary model and fallback model both failed. Fallback error: {fallback_err}")
            else:
                raise e

    except groq.AuthenticationError:
        raise Exception("Invalid Groq API key. Please verify your .env file.")
    except groq.APITimeoutError:
        raise Exception("The request to the Groq API timed out. Please try again.")
    except groq.APIConnectionError:
        raise Exception("Network error occurred while connecting to the Groq API.")
    except Exception as e:
        if "JSON is missing required keys" in str(e) or "malformed response" in str(e):
            raise
        raise Exception(f"An error occurred while analyzing the issue: {str(e)}")
