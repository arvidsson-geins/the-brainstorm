import ollama
import requests
import json
from transformers import AutoTokenizer
from utils import vectorize_data
from utils.output import dump_messages_to_file
from utils.messages import fix_messages

# Dictionary to store indexes and data for each agent
import os
from utils import vectorize_data
instructions_converstional = f"""
Context:
You are in a conversation with the following persons:
[agents]

If suitable ask them directly for their advice or opinion by mentioning their name.
Only address one person at a time to avoid confusion. No other person with same name as you are in the conversation.
Never say your own name in the conversation.
"""    


# Dictionary to store indexes and data for each agent
agent_contexts = {}

def initialize_agent_contexts(agents, base_path = "./index/data/"):
    """
    Initialize FAISS index and context for each agent.
    """
    global agent_contexts

    for agent in agents:
        index_file = os.path.join(base_path, f"{agent.lower()}_index.bin")
        data_file = os.path.join(base_path, f"{agent.lower()}_data.pkl")

        if os.path.exists(index_file) and os.path.exists(data_file):
            # print(f"Loading existing context for {agent}...")
            try:
                index = vectorize_data.load_index(filename=index_file)
                data = vectorize_data.load_data_file(filename=data_file)
                agent_contexts[agent] = {"index": index, "data": data}
                #print(f"Context for {agent} loaded successfully!")
            except Exception as e:
                #print(f"Error loading context for {agent}: {e}")
                agent_contexts[agent] = {"index": None, "data": []}
        else:
            #print(f"No existing context for {agent}. Regenerating...")
            from utils.vectorize_data import regenerate_index_if_missing
            regenerate_index_if_missing(agent, base_path=base_path)
            if not os.path.exists(index_file) or not os.path.exists(data_file):
                print(f"Skipping {agent}: No data available for context.")
                agent_contexts[agent] = {"index": None, "data": []}
                continue
            try:
                index = vectorize_data.load_index(filename=index_file)
                data = vectorize_data.load_data_file(filename=data_file)
                agent_contexts[agent] = {"index": index, "data": data}
                # print(f"Context for {agent} regenerated and loaded successfully!")
            except Exception as e:
                # print(f"Error loading regenerated context for {agent}: {e}")
                agent_contexts[agent] = {"index": None, "data": []}


def get_agent_context(agent_name, base_path = "./index/data/"):
    if agent_name not in agent_contexts or agent_contexts[agent_name]["index"] is None:
        #print(f"Lazy loading context for {agent_name}...")
        index_file = os.path.join(base_path, f"{agent_name.lower()}_index.bin")
        data_file = os.path.join(base_path, f"{agent_name.lower()}_data.pkl")
        
        # check if the files exist
        if not os.path.exists(index_file) or not os.path.exists(data_file):
            #print(f"Skipping {agent_name}: No data available for context.")
            agent_contexts[agent_name] = {"index": None, "data": []}
            return agent_contexts[agent_name]
        try:
            index = vectorize_data.load_index(filename=f"data/{agent_name.lower()}_index.bin")
            data = vectorize_data.load_data_file(filename=f"data/{agent_name.lower()}_data.pkl")
            agent_contexts[agent_name] = {"index": index, "data": data}
        except Exception as e:
            print(f"Error loading context for {agent_name}: {e}")
            agent_contexts[agent_name] = {"index": None, "data": []}
    return agent_contexts[agent_name]


def chat(agent, messages, nr=0, dump_messages=False, agents=[]):

    
    agent_name = agent.getname()
    context = get_agent_context(agent_name)
    index = context["index"]
    data = context["data"]
    
    other_agents = []
    for a in agents:
        if(a.getname() != agent.getname()):
            other_agents.append(a)         
    
    
    # Get the user's latest message
    user_query = messages[-1]['content'] if messages else ""
    
    # Retrieve relevant context using FAISS index
    vector_context = ""
    if index and data:
        vector_context = vectorize_data.query_index(user_query, data, index, k=3)
        vector_context = "\n".join(vector_context)  # Combine results into a single string
    
    # Combine instructions and vectorized context
    agent_context = agent.getInstructions(other_agents) 
    if(vector_context):
        agent_context += "\n\nRelevant Context for users question:\n" + vector_context

    # Fix the messages
        
     # Prepare the messages for the model
    prepped_messages = [{'role': msg['role'], 'content': msg['content']} for msg in messages]       
    prepped_messages = messages
    
    
    # Get the response from the model
    response = agent.chat_model(prepped_messages, relevant_context_text=vector_context, agents=agents)
        
    response = clean_response(response)

    if dump_messages:
        dump_messages_to_file(prepped_messages, response, agent.getname(), nr)
        
    return response

    
def chat_model_w_ollama_generate(agent, model, messages, relevant_context_text="", agents=[]):
    
    messages = fix_messages(messages, agent.getname(), agents=agents)
    
    # get context
    context = get_context_from_last_response(agent.getname())
    # print(f"Context from last response: {context}")
        
    # Get the user's latest message
    # reply_to_user = messages[-1]['speaker'] if messages else ""
    last_message = messages[-1]['content'] if messages else ""
    
    # prompt = print(f"{user_message}")

    # Extract the system message
    system_message = messages[0]['content'] if messages else ""
    # print(f"******** System message: {system_message}")

    # Build the context as a single string from the message history (excluding the system and user messages)
    # remove las message simce its the promt
    messages = messages[:-1]
    messages = limit_conversation_history(messages, max_messages=5)
    history_context = "\n".join(
        f"{msg['role']}: {msg['content']}" for msg in messages[1:-1]
    )
        
    # Combine the relevant context text with the message history
    combined_context = f"{relevant_context_text}\n\nConverasation so far:\n{history_context}".strip()
    combined_context = "You are " + agent.getname() + " in this Converasation.\n" + combined_context
    
    # ????
    tokenized_context = vectorize_data.tokenize_string(combined_context, model)
    # print(f"Tokenized context: {tokenized_context}")
    
    # Prepare the API request
    url = "http://localhost:11434/api/generate"
    headers = {'Content-Type': 'application/json'}
    req_data = {
        "model": model,
        "prompt": last_message,  # The current user query
        "system": system_message,  # System-level instructions
        "context": tokenized_context,  # Full context as a string
        "stream": False  # Disable streaming
    }

    # Make the API request
    response = requests.post(url, headers=headers, data=json.dumps(req_data))
    
    response.raise_for_status()  # Raise an exception for bad status codes
    print(f"*.*.*.*.*.*.*.*.*.*.*.*.")
    print(f"")
    print(f"Chatting with:")
    print(f"Agent: {agent.getname()}")
    print(f"Model: {model}")
    print(f"Relevant context: ")
    print(f"---------------------")
    #print(f"{relevant_context_text}")
    print(f"---------------------")
    print(f"Combined context: ")
    print(f"---------------------")
    #print(f"{combined_context}")
    print(f"---------------------")
    print(f"---------------------")
    print(f"System message: ")
    print(f"---------------------")
    #print(f"{agent.getInstructions(agents)}")
    print(f"---------------------")

    # Handle the response
    converstation_response = agent.getEmptyResponse()
    if response.status_code == 200:
        response_content = response.json().get('response', '')
        # save response json to file
        save_response_to_file(response, agent.getname())
        
        # dump the response to print in a structured way
        # structured_response = json.dumps(response.json(), indent=4)
        #print(f"Response:\n{structured_response}")
        #print(f"Response:\n{response_content}")
        print(f"*.*.*.*.*.*.*.*.*.*.*.*.")
        if(response_content):
            converstation_response = response_content
        
    
    return converstation_response

def chat_model_w_ollama_chat(agent, model, messages, relevant_context_text="", agents=[]):
    # add system message to chat
    chat_msgs = [
        {
            "role": 'system',
            "content": agent.getInstructions(agents) + "\nRelevant Context:\n" + relevant_context_text
        }
      
    ]  
    # add messages to chat 
    for msg in messages:
        if msg['role'] == agent.getname():
            chat_msgs.append({
                "role": 'assistant',
                "content": msg['content']
            })
        else:
            chat_msgs.append({
                "role": 'user',
                "content": msg['content']
            })
           
    
    # Prepare the API request
    url = "http://localhost:11434/api/chat"
    headers = {'Content-Type': 'application/json'}
    req_data = {
        "model": model,
        "messages": chat_msgs,  # The current user query
        "stream": False  # Disable streaming
    }

    # Make the API request
    response = requests.post(url, headers=headers, data=json.dumps(req_data))
    
    response.raise_for_status()  # Raise an exception for bad status codes
   

    # Handle the response
    converstation_response = agent.getEmptyResponse()
    if response.status_code == 200:
        converstation_response = response.json().get('message', '').get('content', '')
        print(f"*.*.*.*.*.*.*.*.*.*.*.*.")       
    return converstation_response
        
    


def clean_response(response):
    # Remove any \n after last character
    response = response.rstrip('\n')
    return response

def getConversationInstructions(agents):
    text = ""    
    for agent in agents:
        text += f"- {agent.getname()}, {agent.getBio()} \n"
    
    # replace [agents] with the list of agents
    instructions = instructions_converstional.replace("[agents]", text)
    return instructions

def save_response_to_file(response, filename):
    filename = filename.lower()
    filename = filename + ".json"
    filename = "response.json"
    filepath = os.path.join("./data/response/", filename)
        
    with open(filepath, 'w') as f:
            json.dump(response.json(), f)

def get_context_from_last_response(agentName):
    agentName = agentName.lower()
    filename = agentName + ".json"
    
    filename = "response.json"
    filepath = os.path.join("./data/response/", filename)
    
    # if file does not exist return empty context
    if not os.path.exists(filepath):
        return []
    
    with open(filepath, 'r') as f:
        response = json.load(f)
        
    # get context from response
    context = response.get('context', [])

    return context
    
def limit_conversation_history(messages, max_messages=5):
    """
    Limit the conversation history to the most recent exchanges.

    Args:
        messages (list): List of conversation messages.
        max_messages (int): Maximum number of messages to include.

    Returns:
        list: Truncated list of messages.
    """
    return messages[-max_messages:]


def truncate_tokens(content, tokenizer, max_tokens=1024):
    """
    Truncate content to ensure it fits within the token limit.

    Args:
        content (str): Input string to truncate.
        tokenizer: The tokenizer used to compute token length.
        max_tokens (int): Maximum allowed tokens.

    Returns:
        str: Truncated content.
    """
    tokens = tokenizer.encode(content, add_special_tokens=False)
    if len(tokens) > max_tokens:
        truncated_tokens = tokens[-max_tokens:]  # Keep only the last `max_tokens`
        return tokenizer.decode(truncated_tokens)
    return content



"""     print(f"---------------------------------------------------------------")    
    print(f"**** CONTEXT Messages:****")
    readble = json.dumps(messages, indent=4)    
    print(f"{readble}")    
    print(f"")
    print(f"PROMT::::")
    print(f"*** NAME::  {agent.getname()}")
    print(f"*** MODEL:: {model}")
    print(f"")
    print(f"REPLY TO::: {user}")
    print(f"{user_message}")
    print(f"---------------------------------------------------------------")    
    print(f"")
    print(f"") """