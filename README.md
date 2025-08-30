#  Your Text, Your Style – AI PowerPoint Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent web application that transforms raw text, prose, or markdown into a fully formatted PowerPoint presentation using the design and style of any user-provided template.

---
##  Live Demo

You can try the live application here: https://spectacular-truffle-324cd7.netlify.app/

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



---
## 🧠 How It Works

This application transforms unstructured text into a styled presentation through a sophisticated two-step process: intelligent content structuring by a Large Language Model (LLM) and precise style application using a backend engine.

### 1. Text Parsing and Slide Mapping

First, the user's raw text input and one-line guidance are sent to the selected LLM (Gemini, OpenAI, or Anthropic). The core of the prompt instructs the model to act as a presentation expert, analyzing the entire text to identify key themes, titles, and hierarchical points. It is specifically asked to return a structured JSON object, typically an array of slides, where each slide has a `title` and a `content` field (often an array of bullet points). The user's guidance heavily influences this process; for example, a request for an "investor pitch" will result in a more concise, impactful structure compared to a "technical summary." This ensures the slide breakdown is not arbitrary but contextually relevant to the user's goal.

### 2. Template Style and Asset Application

Once the structured JSON is received, the backend engine, powered by the `python-pptx` library, takes over. The user's uploaded template file (`.pptx` or `.potx`) is opened and analyzed. The engine inspects the template's **Slide Master** and its various **Slide Layouts** (e.g., 'Title Slide', 'Title and Content', 'Section Header'). It then intelligently iterates through the JSON data from the LLM, matching each slide's content to the most appropriate layout. For instance, a slide with a title and a list of bullet points is mapped to the 'Title and Content' layout. By doing this, the new presentation automatically inherits all the design elements from the template: fonts, color schemes, logos, backgrounds, and even placeholder image positions, ensuring the final output perfectly matches the user's desired style.
