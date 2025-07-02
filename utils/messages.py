def fix_messages(messages, name, agents):
    # If only two agents are in the conversation, set roles accordingly
    if len(agents) == 2:
        return fix_messages_two_part(messages, name)

    # Handle multiple agents
    return fix_messages_many_part(messages, name, agents)

def fix_messages_many_part(messages, name, agents):
    for msg in messages:
        if 'speaker' not in msg:
            msg['speaker'] = msg.get('role', 'user')  # Default to 'user' if 'speaker' is missing
        if 'role' not in msg:
            msg['role'] = msg['speaker']
    return messages

def fix_messages_two_part(messages, name):
    for msg in messages:
        if 'speaker' not in msg:
            msg['speaker'] = msg.get('role', 'user')  # Default to 'user' if 'speaker' is missing
        if msg['speaker'] != name:
            msg['role'] = 'user'
        else:
            msg['role'] = 'assistant'
    return messages
