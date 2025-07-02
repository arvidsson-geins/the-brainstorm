import time
import os
import shutil
from config import OUTPUT_DIR

def dump_conversation_to_file(conversation, final=False):
    """Dump the conversation to a file."""
    # add date and time to the file name
    output_file_name = f'conversation_going.txt'
    if(final):
        output_file_name = f'conversation_{time.strftime("%Y%m%d-%H%M%S")}.txt'
    output_file = os.path.join(OUTPUT_DIR, output_file_name)
    
    exchange = 0
    
    # format the conversation
    with open(output_file, 'w') as f:
        for turn in conversation:
            #check if ts is in the turn
            if 'ts' in turn:
                
                f.write(f"{turn['ts']} - [{exchange}] - {turn['speaker']}: {turn['content']}\n----------------\n")
                exchange += 1
            
    return output_file

    # print(f"Conversation saved to {output_file}")
    
def dump_messages_to_file(messages, reply, name, nr):
    """Dump the messages to a file."""
    # check if directory exists
    if not os.path.exists(os.path.join(OUTPUT_DIR, 'messages')):
        os.makedirs(os.path.join(OUTPUT_DIR, 'messages'))
        
    # add date and time to the file name
    output_file_name = f'{nr}_{name}.txt'
    output_file = os.path.join(OUTPUT_DIR,'messages', output_file_name)
    
    exchange = 0
    
    with open(output_file, 'w') as f:
        for msg in messages:
            f.write(f'role[{msg['role']}] - msg["\n {msg['content']}\n"]\n\n')
            exchange += 1
        f.write(f'\n-------\nREPLY:\n[{name}] - ["\n{reply}\n"]\n')
    
    # print(f"Messages saved to {output_file}")
    
# clear the output directory
def clear_output_dir():
    delete_all_files_in_directory(OUTPUT_DIR)

def delete_all_files_in_directory(directory_path):
    print(f"Cleaning directory: {directory_path}")
    if not os.path.isdir(directory_path):
        raise ValueError(f"Provided path '{directory_path}' is not a directory.")
    
    try:
        for root, dirs, files in os.walk(directory_path, topdown=False):
            # Delete all files
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                #print(f"Deleted file: {file_path}")
            
            # Delete empty directories
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if not os.listdir(dir_path):  # Check if the directory is empty
                    os.rmdir(dir_path)
                    #print(f"Deleted empty directory: {dir_path}")
                    
    except Exception as e:
        raise OSError(f"Error while cleaning directory '{directory_path}': {e}")
