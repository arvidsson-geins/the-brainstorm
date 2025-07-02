from models import eric, max, sam, olivia, chris, jan, patrik, kevin

from chat import start_chat

exchanges = 100000
sleep_duration = 30



# Start the chat session
if __name__ == "__main__":
    # agents = [chris, olivia, jan]
    agents = [patrik, kevin]
    start_chat(agents, num_exchanges=exchanges, sleep_duration=sleep_duration)