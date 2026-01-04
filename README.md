**Javanese Script Translator – Web Interface**

A modern, web-based graphical interface for translating Javanese Script into Latin transliteration and English, built on top of an existing Python translation engine.

✨ Features
🎨 Modern & responsive UI
📱 Mobile-friendly layout
⚡ Real-time translation
📊 Word analysis with morphological breakdown
🔍 Debug mode for detailed processing insight
⌨️ Keyboard shortcuts (Ctrl + Enter)
📝 Example texts for quick testing
📦 Installation

_Install all required Python dependencies:_
- pip install -r requirements.txt
- ▶️ Running the Application
- Start the Flask web server: **python server.py**

**Open your browser and navigate to:** _http://localhost:5000_

The interface will load automatically — you can start translating right away.

🧭 Usage Guide
1. Input
Type or paste Javanese script text into the input field.

2. Translat
Click the Translate button
Or press Ctrl + Enter (Cmd + Enter on macOS)

3. View Results
Latin transliteration appears in the left panel
English translation appears in the right panel
Word analysis table displays detailed morphological breakdown

4. Examples
Use the example buttons to instantly test sample inputs.

5. Debug Mode
Enable Debug Mode to view detailed processing logs in the browser console.

⌨️ Keyboard Shortcuts
Shortcut	Action
Ctrl + Enter	Translate text
Ctrl + R	Translate text
Help Button	View usage instructions
🗂️ Project Structure
├── index.html        # Main web interface
├── style.css         # Styling and layout
├── script.js         # Client-side JavaScript logic
├── server.py         # Flask server & API
├── ct.py             # Core translation engine
├── requirements.txt  # Python dependencies

🔌 API Reference

The application exposes a REST API endpoint:

POST /translate

Request Body

{
  "text": "javanese text",
  "debug": false
}


Response

{
  "latin": "...",
  "english": "...",
  "analysis": [...],
  "errors": []
}

**🛠️ Troubleshooting**
- Ensure the server is running on port 5000
- Check the browser console (F12) for JavaScript errors
- Enable Debug Mode for detailed processing output
- Reinstall dependencies if needed:
- pip install -r requirements.txt

Default server address: http://localhost:5000

Debug output appears in the browser console

Fully responsive and optimized for desktop & mobile

