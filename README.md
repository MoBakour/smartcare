# SmartCare - AI-Powered Smart Wound Dressing Monitoring System

SmartCare is an innovative healthcare monitoring system that combines AI technology with smart wound dressings to provide real-time patient monitoring and analysis. The system helps healthcare providers track wound healing progress, detect potential infections, predict healing times, and receive AI-powered recommendations for patient care.

## Features

-   **Real-time Monitoring**: Track wound dressing sensor data in real-time
-   **AI Analysis**:
    -   Infection detection
    -   Healing time prediction
    -   Patient status analysis
-   **GenAI Integration**: Provides intelligent recommendations and suggestions
-   **Patient Management**: Add and manage patient records
-   **Secure Authentication**: JWT-based secure authentication system

## Technology Stack

### Frontend

-   Vue.js 3 with TypeScript
-   Pinia for state management
-   Tailwind CSS for styling
-   Vue Router for navigation
-   Chart.js for data visualization
-   Vite as build tool

### Backend

-   Python with Flask framework
-   JWT for authentication
-   MongoDB for database
-   Scikit-Learn for machine learning models
-   Google's Gemini API for AI features

## Prerequisites

-   Node.js (v16 or higher)
-   Python 3.8 or higher
-   MongoDB
-   Google Cloud account (for Gemini API)

## Installation

### Backend Setup

1. Navigate to the server directory:

```bash
cd server
```

2. Create and activate a virtual environment:

```bash
python -m venv venv  # On Mac: python3 -m venv venv
venv/bin/activate  # On Mac: source venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt  # On Mac: pip3 install -r requirements.txt
```

4. Create a `.env` file in the server directory with the following variables:

```
DB_NAME = "smartcare"
MONGO_URI = "mongodb+srv://<username>:<password>@<cluster>.mongodb.net"
SECRET_KEY = "<some_secret_value>"
GENAI_API_KEY = "<your_api_key>"
```

### Frontend Setup

1. Navigate to the client directory:

```bash
cd client
```

2. Install dependencies:

```bash
npm install
```

3. Create a `.env` file in the client directory with the following variables:

```
VITE_API_URL = "http://localhost:5173"
```

## Running the Application

### Backend

1. Activate the virtual environment (if not already activated):

```bash
cd server
venv/bin/activate  # On Mac: source venv\Scripts\activate
```

2. Start the Flask server:

```bash
python app.py # On Mac: python3 app.py
```

The backend server will run on `http://localhost:5000`

### Frontend

1. In a new terminal, navigate to the client directory:

```bash
cd client
```

2. Start the development server:

```bash
npm run dev
```

The frontend application will be available at `http://localhost:5173`

## Building for Production

### Frontend

1. Build the frontend application:

```bash
cd client
npm run build
```

The built files will be in the `dist` directory.

### Backend

The backend is ready for production deployment. Make sure to:

1. Set appropriate environment variables
2. Use a production-grade WSGI server (e.g., Gunicorn)
3. Configure proper security measures

## Deployment

### Frontend Deployment

-   Build the frontend using `npm run build`
-   Deploy the contents of the `dist` directory to your web server or cloud platform (e.g., Netlify, Vercel, or AWS S3)
-   Set up environment variables in your deployment platform

### Backend Deployment

-   Deploy the Flask application to a cloud platform (e.g., Render.com, Heroku, AWS, or Google Cloud)
-   Set up environment variables in your deployment platform
-   Configure MongoDB connection
-   Set up proper CORS settings for production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by [Mohamed Bakour](https://bakour.dev)
