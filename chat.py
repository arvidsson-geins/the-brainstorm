import time
# get the models from the models directory
from models import moderator, max, eric
import utils.output as output

# clear output directory
output.clear_output_dir()

# Start the conversation (shared context for both models)
conversation = []

# Number of exchanges
num_exchanges = 3
sleep_duration = 2  # Time between responses (seconds)

print("Starting conversation...")

# Conversation loop
for i in range(num_exchanges):
    try:
        # Determine the current speaker and role
        if i % 2 == 0:
            current_model = max
            other_model = eric
        else:
            current_model = eric
            other_model = max
          
        speaker = current_model.getname()
        
        # if first run start the conversation
        if i == 0:
            conversation.append({'role': other_model.getname(), 'content': other_model.start_conversation, 'speaker': other_model.getname(), 'ts': time.strftime('%H:%M:%S', time.localtime())})
 
        # Generate a response using the current model
        response = current_model.chat(messages=conversation, nr=i, dump_messages=True)
        
        # Get the timestamp of current time
        current_time = time.strftime('%H:%M:%S', time.localtime())

        # Append the response to the shared conversation context
        conversation.append({'role': speaker, 'content': response, 'speaker': speaker, 'ts': current_time})

        # Print the current exchange
        print(f"{current_time} - {speaker}: {response}")
        output.dump_conversation_to_file(conversation, final=False)
        time.sleep(sleep_duration)
        
        # if the last exchange, add a closing message from the other model
        if i == num_exchanges - 1:
            print('Closing message... from the other model')

        
        # if last exchange make moderator summarize the conversation
        if i == num_exchanges - 1:
            moderator.sum_up(conversation, current_model.getname(), other_model.getname())
           
    except Exception as e:
        print(f"Error during chat generation: {e}")
        break

# Print the full conversation to a file if more than 2 turns
conversation_file = output.dump_conversation_to_file(conversation, final=True)
print(f"Conversation saved to {conversation_file}")
print("Conversation completed!")

