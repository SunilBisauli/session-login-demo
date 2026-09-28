# Flask Session Authentication App

A beginner-friendly web application built with Python and Flask that demonstrates session-based authentication, user registration, and SQLite database integration.

## Features
* **User Registration:** Create new accounts safely.
* **Secure Passwords:** Uses `werkzeug.security` to hash passwords before saving them to the database.
* **Session Management:** Logs users in using Flask's secure, encrypted cookies.
* **Protected Routes:** The Dashboard cannot be accessed unless a user is actively logged in.
* **Database Integration:** Automatically creates and uses a local SQLite database (`users.db`).

## Prerequisites
* Python 3.x installed on your machine.
* Flask installed (`pip install flask`).

## How to Run the Application

1. **Clone the repository:**
   ```bash
   git clone <your-github-repo-url>
   cd <your-repository-folder>