# Multi-Agent Conversational AI Platform

## Overview
This project is a multi-agent conversational AI platform where several AI agents, each with unique personalities and expertise, interact with each other in a simulated chat environment. The system leverages vector search (FAISS), context retrieval, and LLMs (via Ollama API) to generate realistic, context-aware conversations. The platform is extensible, allowing for the addition of new agents and data sources.

## Folder Structure
```
chat/
├── chat.py            # Main chat orchestration logic
├── main.py            # Entry point to start a chat session
├── config.py          # Configuration constants (e.g., output directory, API keys)
├── response.json      # (Unused or legacy) JSON response file
├── test.py            # Test and utility functions for development
├── README.md          # Project documentation (this file)
├── models/            # Agent definitions (one file per agent)
├── utils/             # Utility modules (output, Slack integration, vectorization, etc.)
├── output/            # Generated conversation logs and message files
│   └── messages/      # Per-message logs for each agent
├── index/             # FAISS index and data files for each agent
│   └── data/          # Serialized index/data for fast retrieval
├── data/              # 
│   └── <agent>/  # Source data for each agent (txt, md, etc.)
└── .venv/             # Python virtual environment (local, not committed)
```

### Folder Details
- **models/**: Contains Python files for each agent (e.g., `eric.py`, `chris.py`). Each agent has a unique persona, instructions, and chat logic.
- **utils/**: Helper modules for output logging, Slack integration, message formatting, and data vectorization (FAISS, embeddings, etc.).
- **output/**: Stores conversation logs. `conversation_going.txt` is the current session; `messages/` contains per-message logs.
- **index/**: Contains FAISS index and data files for each agent, enabling fast context retrieval.
- **data/**: Raw data for each agent (txt, md, csv, etc.), used to build the agent's knowledge base.
- **.venv/**: Python virtual environment (contains dependencies and Python version info).

## How It Works
- Each agent is defined in `models/` with a unique set of instructions, a bio, and a chat model (LLM backend).
- The system loads data for each agent, vectorizes it, and builds a FAISS index for fast similarity search.
- During a chat session, agents take turns responding. Each response is generated using the agent's LLM, with relevant context retrieved from their own data via FAISS.
- The conversation is logged to `output/` and can be optionally posted to Slack.
- The main entry point is `main.py`, which sets up the agents and starts the chat loop.

## Installation
1. **Clone the repository**
2. **Set up Python 3.12** (required version: **Python 3.12.8**)
3. **Create a virtual environment** (recommended):
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```
4. **Install dependencies**
   - Install the following Python packages (add to `requirements.txt` if needed):
     - `requests`
     - `faiss-cpu`
     - `sentence-transformers`
     - `transformers`
     - `pandas`
     - `PyPDF2`
     - `python-docx`
     - `python-pptx`
   - Example:
     ```bash
     pip install requests faiss-cpu sentence-transformers transformers pandas PyPDF2 python-docx python-pptx
     ```
5. **(Optional) Configure API keys**
   - If using OpenAI or other APIs, set your keys in `config.py`.

## Running the Project
1. **Activate your virtual environment**
   ```bash
   source .venv/bin/activate
   ```
2. **Start the chat session**
   ```bash
   python main.py
   ```
   - By default, the agents to participate are set in `main.py` (edit as needed).
   - The number of exchanges and sleep duration between messages can be configured in `main.py`.

## Output
- **Conversation logs** are saved in `output/conversation_going.txt` (current session) and timestamped files for completed sessions.
- **Per-message logs** are saved in `output/messages/` for debugging and analysis.
- Example output:
  ```
  09:45:36 - [0] - Patrik: Hi, I'm Patrik! Sorry to say but my daughter throw up on me this morning. I'm still here, though!
  ----------------
  09:45:54 - [1] - Kevin: "Well, that's a new one! ..."
  ----------------
  ```

## Agent System
- Each agent is a Python module in `models/` with:
  - A unique name, bio, and instructions
  - A `chat` function for generating responses
  - A `chat_model` function for LLM integration
  - Data files in `data/<agent>/` for context retrieval
- Agents can be added by creating a new file in `models/` and providing data in `data/<agent>/`.

## Python Version
- **Python 3.12.8** is required (see `.venv/pyvenv.cfg`).

## Notes
- The system uses Ollama API for LLM inference (see `test.py` and `models/base.py`).
- Slack integration is available via webhook (see `utils/slack.py`).
- For best results, ensure each agent has relevant data in their `data/` subfolder. 