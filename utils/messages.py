


def fix_messages(messages, name):
    # one message: {'role': 'Ben', 'content': 'ben chat2', 'speaker': 'Ben', 'ts': '17:40:48'}
    # set role to 'user if speaker is not name, if speaker is name set role to 'assistant'
    
    for msg in messages:
        if msg['speaker'] != name:
            msg['role'] = 'user'
        else:
            msg['role'] = 'assistant'
    return messages
    