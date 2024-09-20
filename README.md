
 Work Item Management API

This FastAPI application provides a robust backend for managing users and work items using Firebase Firestore. It includes endpoints for user authentication, work item assignments, and CRUD operations on both users and work items.

 Features

- User Management: Create, retrieve, update, and delete users.
- Work Item Management: Add, update, retrieve, and delete work items.
- User-Work Item Assignment: Assign work items to specific users and track their status.
- CORS Support: Configured to allow cross-origin requests, making it suitable for front-end applications.

 Technologies Used

- FastAPI: A modern, fast web framework for building APIs with Python.
- Firebase Firestore: A NoSQL cloud database for storing and syncing data.
- Pydantic: Data validation and settings management using Python type annotations.
- dotenv: For loading environment variables from a `.env` file.

 Installation

1. Clone the repository:
   bash
   git clone <repository-url>
   cd <repository-name>
   

2. Create a virtual environment and activate it:
   bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   

3. Install the required dependencies:
   bash
   pip install -r requirements.txt
   

4. Set up your Firebase credentials in a `.env` file:
   
   FIREBASE_CREDENTIALS=path/to/your/firebase/credentials.json
   

5. Run the application:
   bash
   uvicorn main:app --reload
   

 API Documentation

Access the automatically generated API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

 Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

 License

This project is licensed under the MIT License. See the LICENSE file for details.
