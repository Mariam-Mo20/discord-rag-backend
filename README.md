# Discord-RAG Backend

Backend API service for the Discord-RAG FAQ Chatbot, built with FastAPI.

## Features

- Receive user queries via `/api/rag-query`  
- Accept and store user feedback via `/api/feedback`  
- Logging of requests and events  
- Ready for future integration with real RAG pipeline  
- Dockerized for easy deployment  

## Requirements

- Python 3.9+  
- Docker (optional, for containerized deployment)  
- Python dependencies listed in `requirements.txt`  

## Local Setup and Run

1. Create and activate a virtual environment:  
   ```bash
   python3 -m venv venv  
   source venv/bin/activate   # On Linux/Mac  
   venv\Scripts\activate      # On Windows  
2. Install dependencies:
   ```bash
   pip install -r requirements.txt  
3. Create a .env file and add your environment variables.
4. Run the application:
   ```bash
   ./run_all.sh

## Running with Docker
1. Build the Docker image:
   ```bash
   docker build -t discord-rag-backend .
2. Run the container:
   ```bash
   docker run -p 5000:5000 --env-file .env discord-rag-backend

## API Endpoints
1. /api/rag-query	  
2. /api/feedback	

## Configuration
Use a .env file to store secrets like tokens and API keys.

## Project Structure
1. main.py: Application entry point
2. discord_bot.py: Discord bot logic
3. rag.py: RAG logic 
4. database.py: Database management for storage
5. requirements.txt: Python dependencies
6. Dockerfile: Docker image build file

## Notes
This project is currently an MVP.
Planned integration with real RAG components for intelligent answers.

## Author
Mariam Mahmoud
