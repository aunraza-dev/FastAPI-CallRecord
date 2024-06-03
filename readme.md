# FastAPI CallRecord

This is a simple FastAPI application that enables two users to connect to a call. When one user presses the "Record" button, the other user receives a notification that the call is being recorded.

## Features
- WebSocket-based communication
- Notification system for call recording status
- Get call duration functionality

## Usage
1. Clone the repository: `git clone https://github.com/aunraza-dev/FastAPI-CallRecord.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the FastAPI server: `uvicorn app:app --reload`
4. Open two browser windows or tabs and navigate to the application's frontend at `http://localhost:8000/static/index.html`
5. Enter the call ID and user ID for each tab and click "Connect"
6. Press the "Record Call" button in one tab to see the notification in the other tab
7. Press the "Get Call Duration" button to see the current call duration

## Technologies Used
- Python
- FastAPI
- WebSocket
- HTML
- JavaScript

Feel free to contribute and improve this project!
