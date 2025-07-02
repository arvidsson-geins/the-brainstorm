import time
from models import eric, max, sam  # Import all agents here
import utils.output as output
import models.base as base
from utils.slack import post_to_slack


def start_chat(agents, num_exchanges=5, sleep_duration=2):
    """
    Handles the chat between multiple agents.

    Args:
        agents (list): List of agent modules to include in the chat.
        num_exchanges (int): Number of exchanges in the chat.
        sleep_duration (int): Time to sleep between exchanges.
    """
    if len(agents) < 2:
        raise ValueError("At least two agents are required to start a chat.")
    
        

    
    # Array of agent names from the agents list
    agent_names = [agent.getname() for agent in agents]
    print(agent_names)

    # Initialize all agent contexts at startup
    base.initialize_agent_contexts(agent_names)

    # Initialize the conversation
    conversation = []

    # Clear the output directory (optional)
    output.clear_output_dir()
    print("")
    print("------------")   
    intro = introduce_agents(agents) 
    intro_msg= {
        'speaker': "Moderator",
        'content': intro,
        'ts':  time.strftime('%H:%M:%S', time.localtime())   
    }
   # post_to_slack(intro_msg)
    print("------------")    
  
    

    
    # Add the first message to the conversation
    conversation.append({
        'role': agents[0].getname(),
        'content': agents[0].start_conversation,
        'speaker': agents[0].getname(),
        'ts': time.strftime('%H:%M:%S', time.localtime())
    })
    # post first message to slack
    post_to_slack(conversation[-1])
    time.sleep(10)


    

    for i in range(num_exchanges):
        #skip first agent
        if i == 0:
            continue
            
        print(f"")
        print(f"****             ****")
        print(f"**** Exchange {i} ****")
        try:
            # Determine the current agent and the next agent
            current_agent = agents[i % len(agents)]

            # current_agent = question_to_agent(current_agent, agents, conversation) 
            
            speaker = current_agent.getname()
            print(f"\n\n**** FINAL Selected current : {speaker} ****\n\n")            
          
            
            # Generate a response using the current agent
            response = current_agent.chat(messages=conversation, nr=i, dump_messages=True, agents=agents)
            #print(f"**** Current agen resonse: {response} ****")

            # Get the timestamp of the response
            current_time = time.strftime('%H:%M:%S', time.localtime())
            
            

            # Append the response to the conversation
            conversation.append({
                'role': speaker,
                'content': response,
                'speaker': speaker,
                'ts': current_time
            })
            
            # Post the response to Slack            
            post_to_slack(conversation[-1])

            # Print the response
            
            #print(f"{current_time} - {speaker}: {response}")

            # Save the ongoing conversation (non-final)
            output.dump_conversation_to_file(conversation, final=False)

            # Pause between exchanges
            time.sleep(sleep_duration)

        except Exception as e:
            print(f"Error during chat: {e}")
            break

    # Save the final conversation
    conversation_file = output.dump_conversation_to_file(conversation, final=True)
    print(f"Conversation saved to {conversation_file}")
    print("Chat completed!")

def question_to_agent(current_agent, agents, conversation):
    print(f"**** Current agent IS GOING TO BE: {current_agent.getname()} ****")   
    
    agent_names = [agent.getname().lower() for agent in agents]
    ##print(agent_names)
    
    # get the last message
    last_message = conversation[-1]    
    print(f"**** Last FULL message: {last_message['content']} ****")
    
    # see if there is a mention of an agent in the last message close to a question
    # if so, return the agent name
    
    # keep only part after   \n or . from the last message     
    last_message_content = last_message['content'].split("\n")[-1].lower()
    
    last_message_content = last_message_content.split(". ")[-1]
    
    # see if there is a question mark in the last message
    #if last_message_content.find("?") < 0:
    #    return current_agent
     
    print(f"**** Looking for agent in question: \n{last_message_content}\n ****")
    
    for agent in agents:

        if agent.getname().lower() in last_message_content and agent.getname().lower() != current_agent.getname():            
            print(f".........**** FOUND agent in question: {agent.getname()} ****")
            return agent   
        
    return current_agent



def introduce_agents(agents):
    """
    Introduces the agents to each other.

    Args:
        agents (list): List of agent modules to introduce.
    """
    retvalue = []
    retvalue.append("Introducing the agents:")   
    #print(agents)  # Debugging statement, can be removed later
    for agent in agents:
        #print(f"Agent: {agent}")  # Debugging statement, can be removed later
        try:
            name = agent.getname()
            bio = agent.getBio() or "No bio available"
            retvalue.append(f"*{name}* {bio}")
        except AttributeError as e:
            print(f"Error with agent: {agent}, missing method. {e}")
        
    # Remove empty lines
    retvalue = [line for line in retvalue if line.strip()]

    # Ensure the function returns the output as a string instead of printing directly
    result = "\n".join(retvalue)
    #print(result)  # Debugging statement, can be removed later
    return result  # Return the final formatted string


def start_chat_2(agents, num_exchanges=5, sleep_duration=2):
    """
    Handles the chat between multiple agents.

    Args:
        agents (list): List of agent modules to include in the chat.
        num_exchanges (int): Number of exchanges in the chat.
        sleep_duration (int): Time to sleep between exchanges.
    """
    
    
    if len(agents) < 2:
        raise ValueError("At least two agents are required to start a chat.")

    # Initialize all agent contexts at startup
    
    #array of agent names from the agents list
    agent_names = [agent.getname() for agent in agents]
    
    base.initialize_agent_contexts(agent_names)

    # Initialize the conversation
    conversation = []

    # Clear the output directory (optional)
    output.clear_output_dir()
    print("")
    print("------------")
    print(f"Starting chat between: {', '.join(agent.getname() for agent in agents)}")

    for i in range(num_exchanges):
        try:
            # Select the current and next agent based on the index
            current_agent = agents[i % len(agents)]
            other_agent = agents[(i + 1) % len(agents)]
            
            speaker = current_agent.getname()

            # If it's the first exchange, start the conversation
            if i == 0:
                conversation.append({
                    'role': other_agent.getname(),
                    'content': other_agent.start_conversation,
                    'speaker': other_agent.getname(),
                    'ts': time.strftime('%H:%M:%S', time.localtime())
                })

            # Generate a response using the current agent
            response = current_agent.chat(messages=conversation, nr=i, dump_messages=True)

            # Get the timestamp of the response
            current_time = time.strftime('%H:%M:%S', time.localtime())

            # Append the response to the conversation
            conversation.append({
                'role': speaker,
                'content': response,
                'speaker': speaker,
                'ts': current_time
            })

            # Print the response
            print(f"{current_time} - {speaker}: {response}")
            
            output.dump_conversation_to_file(conversation, final=False)

            # Pause between exchanges
            time.sleep(sleep_duration)
            

        except Exception as e:
            print(f"Error during chat: {e}")
            break

    # Save the final conversation
    conversation_file = output.dump_conversation_to_file(conversation, final=True)
    print(f"Conversation saved to {conversation_file}")
    print("Chat completed!")


