import ollama
from models import base
from models import jan as current_agent

model = 'codegemma'  # Model focused on generating code
name = "Jan"
bio = "an coding expert who translates discussions into actionable code snippets and provides documentation in Markdown format."

instructions = f"""
Your name is {name}. Your role is to generate high-quality, actionable code snippets and accompanying documentation based on the conversation. Your responses include both functional code and Markdown-formatted documentation.

Core Traits:
1. Code-Driven: Focus on delivering relevant code snippets based on the discussion.
2. Context-Aware: Tailor your responses to the topic at hand, providing meaningful examples.
3. Educative: Explain the implementation clearly using Markdown documentation.

Rules:
1. Always respond with a valid TypeScript code snippet relevant to the topic being discussed.
2. Accompany the code snippet with Markdown documentation explaining its purpose, functionality, and usage.
3. Keep responses concise, focused, and aligned with the conversation.
4. Engage conversationally by summarizing the implementation briefly before presenting the code and documentation.
"""

start_conversation = (
    f"Hi, I'm {name}! I specialize in generating TypeScript code and documentation. "
    "Let me know how I can help with your implementation!"
)
empty_response = "Could you provide more details?"

def getname():
    return name

def getBio():
    return bio

def getInstructions(other_agents=[]):
    """
    Generate instructions dynamically based on other agents in the conversation.
    """
    new_instructions = instructions
    other_agents = [a for a in other_agents if a.getname() != name]
    if other_agents:
        new_instructions += "\n\n" + base.getConversationInstructions(other_agents)
    return new_instructions

def getEmptyResponse():
    return empty_response

def chat(messages, nr=0, dump_messages=False, agents=[]):
    """
    Handles chat interactions for Jan.
    """
    return base.chat(current_agent, messages, nr, dump_messages, agents=agents)

def chat_model(messages, relevant_context_text="", agents=[]):
    """
    Calls Ollama's API to generate code snippets and documentation for Jan.
    """
    # Generate a conversational summary
    conversational_summary = (
        f"Based on the current discussion, here is a relevant TypeScript implementation and its documentation:"
    )

    # Prepare the context for code generation
    code_prompt = f"""
    Generate a TypeScript code snippet based on the following context:
    {relevant_context_text}

    Accompany the code snippet with Markdown documentation explaining:
    1. The purpose of the code.
    2. How it works.
    3. How it can be used.
    """

    # Generate the response
    response = base.chat_model_w_ollama_generate(
        current_agent,
        model,
        [{"role": "user", "content": code_prompt}],
        relevant_context_text=relevant_context_text,
        agents=agents,
    )

    # Return the conversational summary along with the generated response
    if response:
        return f"{conversational_summary}\n\n{response}"
    else:
        return empty_response
