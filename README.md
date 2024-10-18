<div class="hero-icon" align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
</div>

<h1 align="center">
AI-Powered-User-Query-Backend
</h1>
<h4 align="center">A streamlined backend for integrating OpenAI's language models into applications.</h4>
<h4 align="center">Developed with the software and tools below.</h4>
<div class="badges" align="center">
  <img src="https://img.shields.io/badge/Framework-FastAPI-blue" alt="Framework: FastAPI" />
  <img src="https://img.shields.io/badge/Backend-Python-red" alt="Backend: Python" />
  <img src="https://img.shields.io/badge/Database-PostgreSQL-blue" alt="Database: PostgreSQL" />
  <img src="https://img.shields.io/badge/LLMs-OpenAI-black" alt="LLMs: OpenAI" />
</div>
<div class="badges" align="center">
  <img src="https://img.shields.io/github/last-commit/coslynx/AI-Powered-User-Query-Backend?style=flat-square&color=5D6D7E" alt="git-last-commit" />
  <img src="https://img.shields.io/github/commit-activity/m/coslynx/AI-Powered-User-Query-Backend?style=flat-square&color=5D6D7E" alt="GitHub commit activity" />
  <img src="https://img.shields.io/github/languages/top/coslynx/AI-Powered-User-Query-Backend?style=flat-square&color=5D6D7E" alt="GitHub top language" />
</div>

## 📑 Table of Contents
- 📍 Overview
- 📦 Features
- 📂 Structure
- 💻 Installation
- 🏗️ Usage
- 🌐 Hosting
- 📄 License
- 👏 Authors

## 📍 Overview

This repository contains the AI Powered User Queries Backend, a Minimum Viable Product (MVP) built with Python and FastAPI for simplifying AI integration. The MVP provides a lightweight and efficient solution to access OpenAI's powerful language models through a user-friendly API.

## 📦 Features

|    | Feature            | Description                                                                                                        |
|----|--------------------|--------------------------------------------------------------------------------------------------------------------|
| ⚙️ | **Architecture**   | The MVP utilizes a microservice architecture for modularity and scalability, with independent services for query processing, API integration, and database interaction.             |
| 📄 | **Documentation**  | This README provides a comprehensive overview of the MVP's functionality, installation instructions, and usage examples. |
| 🔗 | **Dependencies**   | The MVP relies on libraries like FastAPI, SQLAlchemy, openai, and requests for API development, database management, and OpenAI integration. |
| 🧩 | **Modularity**     | The codebase is organized with separate modules for core services, database interaction, and utility functions. |
| 🧪 | **Testing**        | The MVP includes unit tests for core functions and integration tests for verifying end-to-end functionality.       |
| ⚡️  | **Performance**    | Optimized for efficient query processing and response handling, utilizing caching mechanisms where appropriate. |
| 🔐 | **Security**       | Incorporates best practices for secure development, including data validation, input sanitization, and API key management. |
| 🔀 | **Version Control**| Uses Git for version control and includes a CI/CD pipeline for automated testing and deployment. |
| 🔌 | **Integrations**   | Seamlessly integrates with OpenAI's API for generating responses and utilizes a PostgreSQL database for storing data. |
| 📶 | **Scalability**    | Designed for horizontal scalability by utilizing containerization with Docker and deployment on Kubernetes.           |

## 📂 Structure

```text
ai-query-backend
├── api
│   └── main.py
├── config
│   └── settings.py
├── core
│   ├── services
│   │   └── openai_service.py
│   ├── database
│   │   ├── models.py
│   │   └── database.py
│   └── utils
│       ├── utils.py
│       └── logger.py
└── tests
    └── unit
        ├── test_openai_service.py
        └── test_database.py

```

## 💻 Installation

### 🔧 Prerequisites

- Python 3.9+
- Docker
- Kubernetes (kubectl)
- PostgreSQL

### 🚀 Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/coslynx/AI-Powered-User-Query-Backend.git
   cd AI-Powered-User-Query-Backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` File:
   ```bash
   cp .env.example .env
   ```

4. Configure environment variables:
   Update the `.env` file with your:
    * `DATABASE_URL` (PostgreSQL connection string)
    * `OPENAI_API_KEY` (OpenAI API key)
    * `JWT_SECRET` (secret key for JWT authentication)

5. Build and Run the Application (Docker):
   ```bash
   docker-compose up -d
   ```

6. Deploy to Kubernetes (kubectl):
   ```bash
   kubectl apply -f deployment.yaml
   ```

## 🏗️ Usage

### 🏃‍♂️ Running the MVP

1. Start the development server:
   ```bash
   uvicorn api.main:app --reload
   ```

2. Access the API:
   -  http://localhost:8000/docs for API documentation
   -  http://localhost:8000/redoc for an alternative API documentation view

### ⚙️ Configuration

- **`config/settings.py`:**  Contains configuration settings for database connections, OpenAI API keys, and other essential variables. You can modify these settings based on your specific environment.

### 📚 Examples

**API Endpoints:**

* **POST `/query`**:
    * **Request Body:**
        ```json
        {
          "query": "What is the meaning of life?",
          "model": "text-davinci-003", 
          "temperature": 0.7, 
          "max_length": 256
        }
        ```
    * **Response Body:**
        ```json
        {
          "query_id": "generated_id"
        }
        ```

* **GET `/response/{query_id}`**:
    * **Response Body:**
        ```json
        {
          "response": "The meaning of life is a question that has been pondered by philosophers and thinkers for centuries..."
        }
        ```

## 🌐 Hosting

### 🚀 Deployment Instructions

1. Build a Docker image:
   ```bash
   docker build -t ai-query-backend .
   ```

2. Push the image to a Docker registry (e.g., Docker Hub):
   ```bash
   docker push coslynx/ai-query-backend:latest
   ```

3. Deploy the image to Kubernetes:
   ```bash
   kubectl apply -f deployment.yaml
   ```

### 🔑 Environment Variables

- `DATABASE_URL`: Connection string for the PostgreSQL database
  Example: `postgresql://user:password@host:port/database`
- `OPENAI_API_KEY`: OpenAI API key
  Example: `sk-your-openai-api-key`
- `JWT_SECRET`: Secret key for JWT authentication
  Example: `your-256-bit-secret`

## 📜 API Documentation

### 🔍 Endpoints

* **POST `/query`**:
    * **Description:** Processes a user query using OpenAI's API.
    * **Request Body:**
        ```json
        {
          "query": "What is the meaning of life?",
          "model": "text-davinci-003", 
          "temperature": 0.7, 
          "max_length": 256
        }
        ```
    * **Response Body:**
        ```json
        {
          "query_id": "generated_id"
        }
        ```

* **GET `/response/{query_id}`**:
    * **Description:** Retrieves the response for a given query ID.
    * **Response Body:**
        ```json
        {
          "response": "The meaning of life is a question that has been pondered by philosophers and thinkers for centuries..."
        }
        ```

### 🔒 Authentication

The MVP uses JWT for authentication. To access protected endpoints:

1. Generate a JWT token by registering a new user or logging in.
2. Include the token in the `Authorization` header of requests:

   ```
   Authorization: Bearer YOUR_JWT_TOKEN
   ```

## 📜 License & Attribution

### 📄 License

This Minimum Viable Product (MVP) is licensed under the [GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/) license.

### 🤖 AI-Generated MVP

This MVP was entirely generated using artificial intelligence through [CosLynx.com](https://coslynx.com).

No human was directly involved in the coding process of the repository: AI-Powered-User-Query-Backend

### 📞 Contact

For any questions or concerns regarding this AI-generated MVP, please contact CosLynx at:
- Website: [CosLynx.com](https://coslynx.com)
- Twitter: [@CosLynxAI](https://x.com/CosLynxAI)

<p align="center">
  <h1 align="center">🌐 CosLynx.com</h1>
</p>
<p align="center">
  <em>Create Your Custom MVP in Minutes With CosLynxAI!</em>
</p>
<div class="badges" align="center">
<img src="https://img.shields.io/badge/Developers-Drix10,_Kais_Radwan-red" alt="">
<img src="https://img.shields.io/badge/Website-CosLynx.com-blue" alt="">
<img src="https://img.shields.io/badge/Backed_by-Google,_Microsoft_&_Amazon_for_Startups-red" alt="">
<img src="https://img.shields.io/badge/Finalist-Backdrop_Build_v4,_v6-black" alt="">
</div>