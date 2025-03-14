# Inference Service - DeployForce

## 📌 Overview
The **Inference Service** is a dedicated microservice in the **DeployForce** system, responsible for running AI-based **disaster damage assessments**. It receives **pre-disaster and post-disaster images** and returns **segmentation predictions** for building damage severity.

## 📌 Features
- 🏗 **AI Model Inference**: Processes images and returns damage classification.
- 🔗 **REST API Integration**: Connects with `app_service` to serve AI predictions.
- 📊 **Model Monitoring**: Tracks model performance and updates.
- 📡 **Containerized Deployment**: Easily deployable using Docker.

## 📌 Technologies Used
- **Framework**: Django, Django REST Framework
- **AI Model**: PyTorch, OpenCV, NumPy
- **Containerization**: Docker, Docker Compose
- **Version Control**: Git & GitHub
- **API Communication**: REST API

## 📌 Setup & Installation

### 🔹 Prerequisites
- Python (>=3.8)
- Pipenv (for environment management)
- Docker (if running in containers)
- NVIDIA GPU & CUDA (if using GPU acceleration)

### 🔹 Installation Steps

#### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/your-repository.git
cd services/inference_service
```

#### 2️⃣ Install Dependencies
```bash
pipenv install
```

#### 3️⃣ Load Environment Variables
Create a `.env` file inside `inference_service/`:
```ini
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://user:password@db_host:5432/inference_db
MODEL_PATH=/models/model.pth
```

#### 4️⃣ Run Migrations (If Using a Database)
```bash
pipenv run python manage.py migrate
```

#### 5️⃣ Start the Django Development Server
```bash
pipenv run python manage.py runserver 8001
```

#### 6️⃣ Access the API
Open your browser and go to:
```
http://127.0.0.1:8001/
```

---

## 📌 API Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/predict/` | Receives images and returns segmentation predictions |
| GET | `/health/` | Checks service health |
| GET | `/version/` | Retrieves model version information |

---

## 📌 Running with Docker
Use Docker to containerize the inference service.

#### 1️⃣ Build and Run the Container
```bash
docker build -t inference_service .
docker run -p 8001:8001 --env-file .env inference_service
```

#### 2️⃣ Using `docker-compose`
If using `docker-compose.yml`, navigate to the project root and run:
```bash
docker-compose up --build inference_service
```

---

## 📌 Model Deployment
- Ensure the AI model is placed in `/models/` as specified in `.env`:
```ini
MODEL_PATH=/models/model.pth
```
- The model will automatically be loaded when the service starts.

---

## 📌 Contributing
Contributions are welcome! Please open an issue or submit a pull request.

---

## 📌 License
This project is licensed under the MIT License.

---

## 📌 Contact
📧 **Your Name** - [your.email@example.com](mailto:your.email@example.com)  
🌐 **GitHub** - [your-username](https://github.com/your-username)

---

🚀 **DeployForce Inference Service is now set up!** Let me know if you need any modifications! 🚀
