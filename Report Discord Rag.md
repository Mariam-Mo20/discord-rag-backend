## Technical Assessment – Phase 1 Report  
**Project Title:** Discord RAG FAQ Chatbot  
**Backend Framework:** FastAPI  
**Data Source:** DeepSeek R1 (hosted on Azure)

---

### 1. **Backend Technology Stack Research**  
For the backend, I decided to use **FastAPI** instead of Flask or Node.js/Express, due to its asynchronous capabilities, performance advantages, and better typing support. I also found it simpler to use with modern Python tooling and better suited for rapid prototyping with data-intensive applications.

My data source is **DeepSeek R1**, hosted on Azure. All API calls are served through FastAPI using structured endpoints.

---

### 2. **Deployment Strategy Research**  
I researched various deployment strategies for both local and cloud deployment:

- **Local Deployment:** I created a `Dockerfile` to containerize the entire FastAPI application. This ensures a consistent environment across development and production machines.
  
- **Cloud Deployment (Researched Only):**
  - **Render:** Simple to use for full-stack apps, has free tier, automatic deployment from GitHub.
  - **Heroku:** Easy setup for beginners but limited on free tier.
  - **AWS EC2:** Gives full control but requires manual server management.
  - **Google Cloud Run:** Good for scaling containerized apps.
  - **Verdict:** Render and Google Cloud Run are more developer-friendly for smaller projects.

However, I haven't deployed the project to the cloud yet. It's only tested locally via Docker.

---

### 3. **Logging & Observability (Basic)**  
I implemented basic logging using Python’s `logging` module inside the FastAPI app. It tracks:

- Request handling
- Errors in API responses
- Internal model inference logs (when integrated)

I haven’t added advanced observability features like Prometheus/Grafana or centralized logging tools (e.g., Logstash/ELK), as the scope is currently limited.

---

### 4. **System Architecture Diagram**  
![Architecture Diagram](https://raw.githubusercontent.com/Mariam-Mo20/discord-rag-backend/main/Architecture%20Diagram.png)


### Summary of What’s Done:
-  Selected backend framework (FastAPI)  
-  Used DeepSeek R1 from Azure as the data source  
-  Built API endpoints for RAG logic  
-  Created `Dockerfile` for local deployment  
-  Researched cloud deployment strategies  
-  Set up basic logging with `logging` module  
-  Created system architecture diagram  

---

### Still Pending:
-  No cloud deployment yet  
-  No advanced logging/observability tools  

