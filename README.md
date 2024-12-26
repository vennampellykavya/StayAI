# StayAI

An intelligent assistant for hospitality services, powered by AI Agents and modern Retrieval-Augmented Generation (RAG) systems.

## Overview

StayAI is designed to enhance the hospitality experience by providing automated, intelligent assistance for both guests and service providers. It leverages advanced AI technologies to deliver personalized support and streamline operations.

## Features

- 🤖 AI-powered guest assistance
- 📚 Intelligent information retrieval
- 🏨 Hospitality-specific knowledge base
- 💬 Natural language interaction
- 🔄 Real-time service coordination
- 📊 Analytics and insights

## Getting Started

### Getting started with the repository

1. Fork the repository

2. Clone the repository
```bash
git clone <your-forked-repo-url>
```
3. Install the dependencies
```bash
cd StayAI
```

```python
pip install -r requirements.txt
```

    3.1 Install CrewAI
    ```bash
    cd backend/agents/stay_ai_crew
    ```

    ```bash
    crewai run
    ```

    3.2 Create a .env file and add the following keys:
    - create a .env file in the root directory (StayAI)
    - Copy the env_template.txt file to .env and replace the place-your-key with your actual keys
    ```bash
    cp env_template.txt .env
    ```

    

4. Run the development server
```bash
npm run dev
```

### Prerequisites
 - Python (v3.9 or v3.10)

