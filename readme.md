# Chrome Extension API

This is a FastAPI application designed to work with a Chrome extension. It provides endpoints for text translation and message management.

## Prerequisites

- Python 3.7+
- [OpenAI API Key](https://beta.openai.com/signup/)

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   - On Windows:

     ```bash
     .venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Set up environment variables:**

   Create a `.env` file in the root directory and add your OpenAI API key:

   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

## Running the Application

1. **Start the FastAPI server:**

   ```bash
   uvicorn api.main:app --reload
   ```

   The server will start on `http://localhost:8000`.

## Endpoints

- **GET /**: Check if the API is running.
- **POST /translate**: Translate text to a specified language.
- **POST /messages**: Create a new message.
- **GET /messages**: Retrieve all messages.

## Chrome Extension Setup

1. **Update the `manifest.json` file:**

   Ensure the `host_permissions` in `manifest.json` allow access to your local server:

   ```json:manifest.json
   startLine: 8
   endLine: 10
   ```

2. **Load the extension in Chrome:**

   - Open Chrome and go to `chrome://extensions/`.
   - Enable "Developer mode" in the top right corner.
   - Click "Load unpacked" and select the directory containing your extension files.

## Notes

- This application uses in-memory storage for messages. For production, consider using a database.
- CORS is configured to allow requests from any Chrome extension. Adjust this setting for production use.

## License

This project is licensed under the MIT License.