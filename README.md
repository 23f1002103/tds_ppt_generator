# ✨ Your Text, Your Style – AI PowerPoint Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent web application that transforms raw text, prose, or markdown into a fully formatted PowerPoint presentation using the design and style of any user-provided template.

---
## 🚀 Live Demo

You can try the live application here: **[YOUR_DEPLOYED_APP_LINK_HERE]**

---


---
## 📋 Key Features

* **Intelligent Content Structuring:** Uses your choice of LLM (OpenAI, Anthropic, Gemini) to analyze text and intelligently structure it into slides with titles and bullet points.
* **Dynamic Template Styling:** Automatically inherits the complete look and feel—including fonts, colors, backgrounds, and logos—from any uploaded `.pptx` or `.potx` file by leveraging its Slide Master.
* **User-Provided API Keys:** Ensures privacy and control by allowing users to provide their own LLM API keys, which are never stored or logged.
* **Simple Web Interface:** A clean, easy-to-use interface for pasting text, uploading a template, and downloading the final presentation.
* **Flexible and Adaptable:** Works with a wide variety of templates, from simple designs to complex corporate branding.

---
## 🛠️ Technology Stack

* **Backend:** Python, FastAPI, Uvicorn
* **PowerPoint Engine:** `python-pptx`
* **LLM Integration:** `openai`, `anthropic`, `google-generativeai`
* **Frontend:** HTML5, CSS3, JavaScript

---
## ⚙️ Setup and Usage

To run this project locally, follow these steps:

### Prerequisites
* Python 3.8+
* An LLM API key (OpenAI, Anthropic, or Google)

### 1. Clone the Repository
```bash
git clone [https://github.com/](https://github.com/)[YOUR_GITHUB_USERNAME]/[YOUR_REPO_NAME].git
cd [YOUR_REPO_NAME]
```

### 2. Set Up the Backend
Navigate to the `backend` folder and install the required Python packages.

```bash
cd backend
pip install -r requirements.txt
```
To run the backend server, use Uvicorn:
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### 3. Set Up the Frontend
Navigate to the `frontend` folder in a separate terminal.

```bash
cd frontend
```
Start the simple Python HTTP server:
```bash
python -m http.server 3000
```
Open your web browser and go to `http://localhost:3000` to use the application.

---
## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.