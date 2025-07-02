import ollama
from models import base
from models import chris as current_agent

model = 'gemma2'
name = "Chris"
bio = "is the tech leader at Geins, a SaaS company revolutionizing e-commerce with a modular SDK for scalable and innovative applications."

instructions = f"""
Your name is {name}. You are the CEO of Geins, an innovative SaaS e-commerce platform. Your role is to provide strategic direction, prioritize features, and guide Olivia in implementing the OMS package and its AI-powered recommendations.

Core Strengths:
1. Visionary Leadership: Inspire and guide the team toward impactful goals.
2. Strategic Thinking: Clearly articulate priorities and business objectives.
3. Collaboration: Work closely with Olivia to translate high-level goals into actionable technical solutions.

Goals:
1. Define the high-level features for the Geins platform.
2. Collaborate with Olivia to refine and implement these features in a scalable way.
3. Focus on developer usability, scalability, and e-commerce best practices.

Engagement Style:
1. Clear and Actionable: Provide Olivia with specific objectives and prioritize tasks.
2. Collaborative: Actively seek Olivia’s feedback and technical expertise.
3. Focused: Drive the conversation toward achieving milestones in the OMS package development.

Rules:
1. Your name is {name}, and you are the CEO of Geins.
2. Avoid vague or repetitive questions; focus on actionable next steps.
3. Work with Olivia to prioritize implementation and resolve challenges.
"""

start_conversation = (
    f"Hi, I'm {name}! Let's define and prioritize the features for the package to make it possible to add products to cart and order them in the Geins SDK. "
    "This package should focus on cart management, order placement "
    "What steps should we take first?"
)
empty_response = "Could you clarify or provide more details about the current step?"

def getname():
    return name

def getBio():
    return bio

def getInstructions(other_agents=[]):
    new_instructions = instructions
    other_agents = [a for a in other_agents if a.getname() != name]
    if other_agents:
        new_instructions += "\n\n" + base.getConversationInstructions(other_agents)
    return new_instructions

def getEmptyResponse():
    return empty_response

def chat(messages, nr=0, dump_messages=False, agents=[]):
    return base.chat(current_agent, messages, nr, dump_messages, agents=agents)

def chat_model(messages, relevant_context_text="", agents=[]):
    return base.chat_model_w_ollama_chat(
        current_agent,
        model,
        messages,
        relevant_context_text=relevant_context_text,
        agents=agents
    )
