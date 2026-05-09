# 🏥 Medical Chatbot - REACT & Flask

This repository contains a **medical chatbot** built using a **React frontend** and a **Flask backend**. The chatbot extracts data from locally stored PDFs and provides medical-related responses using AI.

---

## 🛠 Tech Stack

### 🌐 Frontend:
- React.js (with Axios for API requests)
- Custom CSS for styling
- React Toastify for notifications

### ⚙️ Backend:
- Flask (Python)
- OpenAI API for chatbot responses
- LangChain for text processing
- Pinecone for vector storage
- PyPDF for PDF processing

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Barnik-Podder/MediBot.git


### 2️⃣ Backend Setup

#### Create a Virtual Environment
```bash
conda create -n medibot python=3.10 -y
conda activate medibot 
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```
### Setup Environment Variables
Create a .env file in the backend directory and add the required environment variables:
PINECONE_API_KEY=
OPENAI_API_KEY=
BASE_URL =
INDEX_NAME =

#### Run Flask Locally
```bash
python app.py
```

### 3️⃣ Frontend Setup

#### Navigate to the frontend directory
```bash
cd frontend
```

#### Install Dependencies
```bash
npm install
```
### Setup Environment Variables
Create a .env file in the backend directory and add the required environment variables:
REACT_APP_API_URL=

#### Start the React App
```bash
npm start
```

---

## 📄 API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| GET    | `/`     | Health check |
| POST   | `/get`  | Chatbot API |

---

## 🎯 Troubleshooting

### 🔍 Backend Issues
- Ensure `requirements.txt` is correctly installed.
- If Flask doesn't start, check for missing dependencies.
- Verify that the OpenAI API key is set correctly.

### 🔍 Frontend Issues
- If React fails to start, check for missing dependencies with `npm install`.
- Ensure the backend is running before making API requests.

---

## 🌟 Contributing
1. Fork the repo
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Added new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a Pull Request

---

## 📜 License
This project is licensed under the MIT License.

---

**Made with ❤️ by Bipasha**

