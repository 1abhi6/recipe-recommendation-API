# Recipe Recommendation API

_A FastAPI-powered Recipe Generator, leveraging Microsoft Autogen, OpenAI GPT models, Redis DB, and Docker for seamless deployment._

---

## 🚀 Overview

This API lets you generate and recommend recipes using advanced AI (OpenAI's GPT models via Microsoft Autogen). Redis is used as the backend database for fast, scalable data storage. The project is containerized with Docker for simple deployment and local development.

---

## 🛠️ Features

- **Recipe Generation:** Uses OpenAI GPT models via Microsoft Autogen for creative, accurate recipes.
- **RESTful API:** Built with FastAPI for speed and ease of use.
- **Redis Database:** Stores recipes and metadata for quick access.
- **Dockerized:** Easily run anywhere with Docker.
- **Configurable:** Environment variables managed via `.env.example`.

---

## 📦 Quickstart

### 1️⃣ Run with Docker (Recommended)

You can run the API instantly using Docker. No need to install dependencies or set up Python environments!

1. **Copy and Edit `.env` file:**

   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI and Redis credentials if needed
   ```

2. **Pull and Run Docker image:**

   ```bash
   docker pull <docker-hub-username>/recipe-recommendation-api:latest
   docker run --env-file .env -p 8000:8000 <docker-hub-username>/recipe-recommendation-api:latest
   ```

   > _Replace `<docker-hub-username>` with your actual Docker Hub username._

3. **API is now live at:** [http://localhost:8000](http://localhost:8000)

---

### 2️⃣ Manual Setup (Development)

If you want to work with the code or customize, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/1abhi6/recipe-recommendation-API.git
   cd recipe-recommendation-API
   ```

2. **Set up virtual environment (.venv):**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies (using `uv` and `pyproject.toml`):**

   ```bash
   pip install uv
   uv pip install -r requirements.txt
   # OR, if using pyproject.toml
   uv pip install -e .
   ```

4. **Configure environment:**

   ```bash
   cp .env.example .env
   # Edit .env with your API keys and Redis config
   ```

5. **Run the API locally:**

   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at: [http://localhost:8000](http://localhost:8000)

---

## ⚙️ Configuration

- All environment configs are managed via `.env` file. See `.env.example` for available variables.
- You need valid OpenAI API keys and Redis connection details.

---

## 🧪 Testing

- Once running, explore API docs at [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI).
- Try out endpoints and generate recipes interactively!

---

## 📚 Tech Stack

- **FastAPI** (Python)
- **Microsoft Autogen**
- **OpenAI GPT Models**
- **Redis**
- **Docker**

---

## 🙌 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

[MIT](LICENSE)

---

## 🤝 Credits

- Built by [@1abhi6](https://github.com/1abhi6)

---

> _For any issues or bugs, please open an issue on the [GitHub repo](https://github.com/1abhi6/recipe-recommendation-API/issues)._
