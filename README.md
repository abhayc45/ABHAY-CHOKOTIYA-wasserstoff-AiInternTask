# Document Chatbot

This project is a chatbot that can ingest documents and answer questions based on their content.

## Setup

### 1. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 2. Install PaddleOCR

This project uses PaddleOCR to extract text from images. You need to install it on your system.

*   **Windows:**
    *   Follow the official [PaddleOCR installation guide for Windows](https://github.com/PaddlePaddle/PaddleOCR/blob/main/doc/doc_en/installation_en.md).

*   **macOS:**
    *   Follow the official [PaddleOCR installation guide for macOS](https://github.com/PaddlePaddle/PaddleOCR/blob/main/doc/doc_en/installation_en.md).

*   **Linux:**
    *   Follow the official [PaddleOCR installation guide for Linux](https://github.com/PaddlePaddle/PaddleOCR/blob/main/doc/doc_en/installation_en.md).

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