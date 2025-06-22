import requests
import json
from config import OLLAMA_API_URL, OLLAMA_MODEL

def get_ollama_response(prompt: str):
    """
    Sends a prompt to a local Ollama LLM and attempts to parse a JSON response.

    Args:
        prompt (str): The prompt to send to the LLM.

    Returns:
        A tuple containing:
        - dict: The parsed JSON response from the LLM.
        - str: An error message if something goes wrong, otherwise None.
    """
    headers = {'Content-Type': 'application/json'}
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"  
    }
    model_output_text = "" 

    try:
        response = requests.post(OLLAMA_API_URL, headers=headers, json=payload, timeout=300)
        response.raise_for_status()

        result = response.json()
        model_output_text = result.get('response', '')

        parsed_json = json.loads(model_output_text)
        return parsed_json, None

    except requests.exceptions.Timeout:
        return None, f"Ollama API request timed out. The model '{OLLAMA_MODEL}' might be taking too long."
    except requests.exceptions.ConnectionError:
        return None, f"Could not connect to Ollama at {OLLAMA_API_URL}. Please ensure Ollama is running."
    except requests.exceptions.RequestException as e:
        return None, f"API request error: {e}"
    except json.JSONDecodeError as e:
        error_message = (
            "Failed to parse JSON response from Ollama. The model may have returned improperly formatted text.\n"
            f"Error: {e}\n\n"
            f"Model Output Preview:\n---\n{model_output_text[:500]}..."
        )
        return None, error_message
    except Exception as e:
        return None, f"An unexpected error occurred: {e}"