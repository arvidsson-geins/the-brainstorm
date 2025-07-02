import json
import requests
from models.base import initialize_agent_contexts
from models import eric, max, sam
import models as models
from models import base

def chat_model(prompt, model="llama3.2", stream=False):
    """
    Calls Ollama's API to generate a response for the given prompt.
    """
    print("Sending request to Ollama API...")
    url = "http://localhost:11434/api/generate"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print(f"HTTP Status Code: {response.status_code}")

        if response.status_code == 200:
            response_content = response.json()
            print("Raw API Response:")
           #  print(json.dumps(response_content, indent=4))
            return response_content
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def test_chat_model(model):
    """
    Test function to simulate a conversation and verify chat_model functionality.
    """
    print("Running test for chat_model...")

    # Define the prompt
    prompt = "What color is the sky at different times of the day? Respond using JSON."

    # Call the chat_model function
    response = chat_model(prompt, model=model)

    # Check if the response is valid and parse it
    if response and "response" in response:
        try:
            # Parse the JSON response content
            # Parsed_response = json.loads(response["response"])
            print("Parsed Response:")
            print(response)
            #print(json.dumps(parsed_response, indent=4))
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
    else:
        print("Test failed. No valid response received.")
        
def test_index_create():
    print("Running test for index creation...")
    initialize_agent_contexts()
    print("Test complete.")

test_model2 = "wizardlm2:7b"
test_model = 'gemma2:latest'

def testInstructions():
    print("Running test for instructions...")
    agents = [eric, max, sam]
    instructions = base.getConversationInstructions(agents)
    print(instructions)


# Entry point for the test script
if __name__ == "__main__":
    #test_chat_model(test_model)
    #test_chat_model(test_model2)
    # test_index_create()
    testInstructions()
