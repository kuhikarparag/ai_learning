# Disease Prediction Application (Flask + Gemini API)

## Overview
This application predicts possible diseases, suggests medicines (with confidence and dosage frequency), and recommends home remedies (by dietary category and generic) based on user input (gender, age, symptoms) using the Gemini API. It features a modern web frontend (Flask + Bootstrap), robust backend, and a CLI tool for predictions. The codebase is modular, developer-friendly, and easy to set up.

## Features
- Modern Bootstrap web interface (responsive, landscape layout)
- Predicts top 3 diseases (with confidence, info link)
- Suggests medicines (with confidence and times per day)
- Recommends home remedies (disease-specific by dietary category, generic, with medicine mentions)
- Robust Gemini API integration with modular Python prompt files
- Defensive error handling and debug logging
- Easy setup and clear developer documentation

## Setup Instructions

### 1. Clone the Repository
```sh
git clone <repo-url>
cd disease_prediction
```

### 2. Create and Activate a Virtual Environment (Windows)
```sh
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root with your API keys:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
- **GEMINI_API_KEY**: Get from [Google AI Studio](https://aistudio.google.com/app/apikey). You must have a Google account. Go to the API Keys section, create a new key, and paste it in your `.env` file as shown above.

### 5. Run the Flask Application
```sh
python app.py
```
Or use the VS Code task:
- Press `Ctrl+Shift+B` and select `Run Flask App`

The app will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000)

## File Structure
- `app.py` - Flask backend (Gemini integration, robust error handling)
- `templates/index.html` - Bootstrap web frontend (modern, tabbed, responsive)
- `prompt_medicine.py` - Python prompt for medicines (with confidence and times per day)
- `prompt_disease.py` - Python prompt for diseases
- `prompt_remedies.py` - Python prompt for remedies (dietary categories, medicine mentions, disease name)
- `curl.py` - Sample Gemini API call (for direct testing)
- `requirements.txt` - Python dependencies
- `README.md` - This file
- `.env` - API keys (not versioned)

## Developer Notes

### Prompts
- Prompts are Python modules (`prompt_*.py`), not .txt files. They use string formatting and are imported in the backend for robust, maintainable prompt engineering.
- To add new prompts or change output structure, edit the relevant `prompt_*.py` file and update the backend parsing logic in `app.py`.

### API Keys
- Only the Gemini API key is required for core functionality. Never commit `.env` to version control.
- To get a Gemini API key:
  1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
  2. Sign in with your Google account.
  3. Click "Create API Key" and copy the generated key.
  4. Paste it in your `.env` file as `GEMINI_API_KEY=...`.

### Error Handling
- The backend is defensive against missing/invalid Gemini responses and template variable issues. Check logs for details.
- If you see blank results or errors, check your API keys, console/logs, and ensure all dependencies are installed.

### UI/UX
- The frontend uses Bootstrap for a modern, landscape, two-column layout.
- Results are shown in tabbed tables, with remedies grouped by dietary category and medicine mentions highlighted.
- Each tab (Diseases, Medicines, Remedies) includes a summary for quick reference.
- All remedies are shown as ordered lists for clarity.

### Extending
- To add new features, create new prompt files and update the backend logic in `app.py`.
- For new UI features, edit `templates/index.html` and update the JavaScript as needed.

### Troubleshooting
- If you see blank results or errors:
  - Check your API key in `.env`.
  - Ensure all dependencies are installed (`pip install -r requirements.txt`).
  - Check the console/logs for error messages.
  - Make sure your internet connection is active (Gemini API is cloud-based).

## Critical Pointers
- **Never commit your `.env` file or API keys to version control.**
- **Keep your Gemini API key secure.**
- **Update dependencies regularly for security and compatibility.**
- **Test the app after any prompt or backend logic change.**
- **Use the summaries in each tab for a quick overview of results.**

## License
MIT License
