# **Javanese Script Translator – Web Interface**

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20API-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![UI](https://img.shields.io/badge/UI-Responsive-purple)
![License](https://img.shields.io/badge/License-Academic-lightgrey)

A modern, web-based graphical interface for translating **Aksara Jawa** into **Latin transliteration** and **English**, built on top of a compiler-inspired Python translation engine.

---

## ✨ Features

- 🎨 **Modern & responsive UI**
- 📱 **Mobile-friendly layout**
- ⚡ **Real-time translation**
- 📊 **Word-level morphological analysis**
- 🔍 **Debug mode** for detailed lexical and syntactic insight
- ⌨️ **Keyboard shortcuts** (Ctrl + Enter)
- 📝 **Built-in example texts** for quick testing

---

## 📦 Installation

Install all required Python dependencies:
```bash
pip install -r requirements.txt
```

## ▶️ Running the Application

Start the Flask web server:
```bash
python server.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

The interface will load automatically. You can start translating immediately.

---

## 🧭 Usage Guide

### 1. Input
Type or paste Javanese script text into the input field.

### 2. Translate
Click the **Translate** button

### 3. View Results
- Latin transliteration appears in the left panel
- English translation appears in the right panel
- A word analysis table displays morphological breakdown and dictionary lookup

### 4. Examples
Use the example buttons to instantly test predefined inputs.

### 5. Debug Mode
Enable **Debug Mode** to view detailed processing logs (lexer, parser, and validation stages) in the browser console.

---

## 🗂️ Project Structure
```
├── index.html        # Main web interface
├── style.css         # Styling and layout
├── script.js         # Client-side JavaScript logic
├── server.py         # Flask server & REST API
├── ct.py             # Core translation engine (compiler-based)
├── requirements.txt  # Python dependencies
```

---

## 🔌 API Reference

### Endpoint
```
POST /translate
```

### Request Body
```json
{
  "text": "javanese text",
  "debug": false
}
```

### Response
```json
{
  "latin": "...",
  "english": "...",
  "analysis": [...],
  "errors": []
}
```

---

## 🛠️ Troubleshooting

- Ensure the server is running on port 5000
- Check the browser console (F12) for JavaScript errors
- Enable **Debug Mode** for detailed processing output
- Reinstall dependencies if necessary:
```bash
pip install -r requirements.txt
```

- **Default server address:** `http://localhost:5000`
- **Debug output:** Browser console
- **Platform support:** Desktop & Mobile (fully responsive)

---

✨ **Built for educational and linguistic exploration of Aksara Jawa**
