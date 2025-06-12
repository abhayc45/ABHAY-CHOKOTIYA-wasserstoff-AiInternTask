# Document Chatbot

This project is a chatbot that can ingest documents and answer questions based on their content.

## Setup

### 1. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```
hello abhay f
### 2. Install Tesseract OCR

This project uses Tesseract OCR to extract text from images. You need to install it on your system.

*   **Windows (Detailed Steps):**
    1.  **Download the Installer:** Go to the [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) page, which is the official source for Windows installers. Download the `tesseract-ocr-w64-setup-v5.x.x.exe` file.
    2.  **Run the Installer:** Run the downloaded installer. **During installation, it is highly recommended to check the box for "Add Tesseract to system PATH"**. This will automate the most difficult step.
    3.  **If You Missed the PATH Step:** If you did not check the box during installation, you must add it manually:
        *   Find the Tesseract installation folder. By default, it is `C:\Program Files\Tesseract-OCR`.
        *   Search for "Edit the system environment variables" in the Windows Start Menu and open it.
        *   Click the "Environment Variables..." button.
        *   In the "System variables" section, find the `Path` variable, select it, and click "Edit...".
        *   Click "New" and paste in the path to your Tesseract installation folder (e.g., `C:\Program Files\Tesseract-OCR`).
        *   Click OK on all windows to save the changes.
    4.  **Restart VS Code and Terminals:** After installing and setting the PATH, you **must** completely close and reopen VS Code and your terminals for the changes to take effect.

*   **macOS (Homebrew):** `brew install tesseract`
*   **Linux (apt):** `sudo apt-get install tesseract-ocr`

### 3. Set up Google API Key

The application uses Google's Gemini model for embeddings and language generation. You need to have a Google API key.

1.  Get your API key from the [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Create a `.env` file in the root of the project by copying the `.env.example` file:
    ```bash
    cp .env.example .env
    ```
3.  Open the `.env` file and add your Google API key:
    ```
    GOOGLE_API_KEY="your_google_api_key_here"
    ```

### 4. A Note on API Usage

The Google Gemini API has a free tier that is suitable for development and most personal projects. For detailed information on usage limits and pricing, please refer to the [official Google AI pricing page](https://ai.google.dev/pricing).

### 5. Troubleshooting

**Error: `Failed to generate embedding. Check your API key and network connection.`**

This is the most common error and it almost always means there is an issue with your Google API key setup. Here’s how to fix it:

1.  **Verify Your `.env` File:**
    *   Make sure you have a file named exactly `.env` in the root directory (`C:\Users\Aman chopra\Desktop\PROJECT`). It should **not** be `.env.txt` or `.env.example`.
    *   The content of the file should be a single line: `GOOGLE_API_KEY=your_actual_api_key_here`

2.  **Check Your API Key:**
    *   Go back to the [Google AI Studio](https://aistudio.google.com/app/apikey) and double-check that your key is active.
    *   Copy the key again carefully. Make sure there are no extra spaces or characters at the beginning or end.

3.  **Restart the Server:**
    *   After you have verified the `.env` file and the key, **stop** the `uvicorn` backend server (press `Ctrl+C` in its terminal) and restart it. The server only reads the `.env` file when it first starts.

## How to Run

You need to run two components in separate terminals: the backend server and the frontend application.

### 1. Run the Backend

Navigate to the project's root directory and run the FastAPI server:

```bash
uvicorn backend.main:app --reload
```

The backend will be running at `http://localhost:8000`.

### 2. Run the Frontend

In a new terminal, navigate to the project's root directory and run the Streamlit app:

```bash
streamlit run frontend/app.py
```

The frontend will be accessible in your web browser, usually at `http://localhost:8501`.

## How to Use

1.  Open the Streamlit app in your browser.
2.  Upload one or more documents (PDF, PNG, JPG, TXT).
3.  Once the files are uploaded, you can ask a question in the text box.
4.  The chatbot will return the most relevant document excerpts.