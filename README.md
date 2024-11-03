# Customer Review Sentiment Analysis

This project consists of a FastAPI backend for sentiment analysis and a React frontend interface.

## Project Structure

```
CustReview/
├── frontend/         # React + TypeScript frontend
└── model.py         # FastAPI backend
```

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## Backend Setup

1. Navigate to the CustReview directory:
```bash
cd CustReview
```

2. Install Python dependencies:
```bash
pip install fastapi uvicorn scikit-learn numpy pandas
```

3. Start the backend server:
```bash
uvicorn model:app --reload --port 8000
```

The backend will be running at `http://localhost:8000`

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be running at `http://localhost:5173` (or similar port shown in the terminal)

## Usage

1. Make sure both backend and frontend servers are running
2. Open your browser and go to `http://localhost:5173`
3. Enter a customer review in the text input
4. Click "Analyze" to see the sentiment analysis result

## API Endpoints

- POST `/predict`
  - Accepts JSON with a `text` field
  - Returns sentiment analysis score

## Troubleshooting

If you encounter any issues:

1. Ensure all dependencies are installed correctly
2. Check that both servers are running on the correct ports
3. Look for any error messages in the terminal windows
4. Make sure there are no CORS issues (backend should allow frontend origin)

For any other issues, please check the error logs in the respective terminal windows.

## Docker Deployment

To run the application using Docker:

1. Make sure Docker and Docker Compose are installed on your system
2. Navigate to the project root directory
3. Build and start the containers:
```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost
- Backend API: http://localhost:8000

To stop the containers:
```bash
docker-compose down
```