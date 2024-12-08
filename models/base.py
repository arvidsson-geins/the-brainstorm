
from utils.output import dump_messages_to_file
from utils.messages import fix_messages

def chat(agent, messages, nr=0, dump_messages=False):
    # Fix the messages
    messages = fix_messages(messages, agent.getname())
    # Prepare the messages for the model
    prepped_messages = [{'role': msg['role'], 'content': msg['content']} for msg in messages]
    prepped_messages.insert(0, {'role': 'system', 'content': agent.instructions })
    
    # Get the response from the model
    response = agent.chat_model(prepped_messages)
    response = clean_response(response)

    if dump_messages:
        dump_messages_to_file(prepped_messages, response, agent.getname(), nr)
        
    return response

def clean_response(response):
    # Remove any \n after last character
    response = response.rstrip('\n')
    return response
