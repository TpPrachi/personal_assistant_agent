# Personal Assistant Agent

A simple AI-powered Personal Assistant Agent built with **FastAPI**. It supports Anthropic models and can also be configured to run locally using **Ollama**.

---

## Prerequisites

Make sure Python 3 is installed.

```bash
python3 --version
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/TpPrachi/personal_assistant_agent.git
cd personal_assistant_agent
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

**macOS / Linux**

```bash
source venv/bin/activate
```

Once activated, your terminal prompt will display:

```text
(venv)
```

---

## Install Dependencies

Install the required Python packages:

```bash
pip install fastapi uvicorn anthropic python-dotenv
```

Verify the installation:

```bash
python3 -m pip show fastapi
```

If needed, reinstall:

```bash
pip install fastapi uvicorn
```

---

## Environment Variables

Create a `.env` file in the project root.

```bash
touch .env
```

Add your Anthropic API key:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

---

## Running the Application

Start the FastAPI server:

```bash
python3 -m uvicorn main:app --reload
```

or

```bash
uvicorn main:app --reload
```

Using `python3 -m uvicorn` ensures the server runs with the same Python interpreter where your dependencies are installed.

The application will be available at:

```
http://localhost:8000
```

---

# Running with Ollama (Local LLM)

If you prefer to run the application with a local model instead of Anthropic, install Ollama.

### Pull a model

```bash
ollama pull llama3.2
```

or

```bash
ollama pull qwen3
```

### Start the Ollama server

```bash
ollama serve
```

By default, Ollama listens on:

```
http://localhost:11434
```

### Install the Ollama Python client

```bash
python3 -m pip install ollama
```

---

## Test the API

Send a request to the application:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is an AI agent?"}'
```

---

## Tech Stack

- Python 3
- FastAPI
- Uvicorn
- Anthropic SDK
- Ollama (optional)
- python-dotenv

---

## Project Structure

```
personal_assistant_agent/
│
├── main.py
├── .env
├── requirements.txt
├── README.md
└── venv/
```

---

### Google Cloud Setup

1. Go to Google Cloud Console:
console.cloud.google.com

2. Create a new project:

Click the project dropdown at the top
Click New Project
Name it personal-agent
Click Create

3. Enable Gmail API:

Go to APIs & Services → Library
Search Gmail API → click it → click Enable
Search Google Calendar API → click it → click Enable

4. Create OAuth credentials:

Go to APIs & Services → Credentials
Click Create Credentials → OAuth Client ID
If asked to configure consent screen first:
Click Configure Consent Screen
Choose External
Fill in App name: Personal Agent
Add your Gmail as test user
Save and continue through all steps
Back in Credentials → Create Credentials → OAuth Client ID
Application type: Desktop App
Name: personal-agent
Click Create
Click Download JSON → save as credentials.json in your project folder

---

## License

This project is intended for learning and experimentation.