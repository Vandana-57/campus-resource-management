\# Campus Resource Management System



A web-based Campus Resource Management System designed to provide a centralized platform for students, faculty, and administrators to access and manage campus resources.



\## 1. Project Overview



The Campus Resource Management System simplifies campus resource management by allowing users to view available resources, request bookings, manage their reservations, and report incidents through a centralized application.



The system provides authentication, resource management, booking management, administration, incident reporting, and notifications.



\## 2. Key Features



\- User registration and login

\- JWT-based authentication

\- User profile management

\- Campus resource listing

\- Resource booking and cancellation

\- Booking history

\- Administrator management

\- Incident reporting and management

\- Notification management

\- PostgreSQL database integration

\- REST API-based communication



\## 3. Technology Stack



| Component | Technology |

|---|---|

| Frontend | React.js 19 |

| Build Tool | Vite |

| Programming Language | JavaScript |

| Routing | React Router |

| HTTP Client | Axios |

| Backend | Python Flask |

| API | REST APIs |

| Database | PostgreSQL |

| ORM | SQLAlchemy |

| Authentication | Flask-JWT-Extended |

| Testing | Pytest |

| Code Coverage | Coverage.py |

| Version Control | Git and GitHub |



\## 4. System Architecture



The application follows a three-tier architecture.



1\. \*\*Presentation Layer:\*\* React frontend, pages, components, and user interface.

2\. \*\*Application Layer:\*\* Flask REST API, route blueprints, authentication, and business logic.

3\. \*\*Data Layer:\*\* PostgreSQL database accessed through SQLAlchemy models.



\### Application Flow



User → React Frontend → REST API → Flask Backend → SQLAlchemy → PostgreSQL



\## 5. Project Structure



```text

campus-resource-management/

│

├── backend/

│   ├── routes/

│   ├── utils/

│   ├── app.py

│   ├── models.py

│   ├── extensions.py

│   ├── create\_admin.py

│   ├── requirements.txt

│   └── test\_\*.py

│

├── frontend/

│   ├── public/

│   ├── src/

│   ├── package.json

│   └── vite.config.js

│

├── database/

│   ├── schema.sql

│   └── seed.sql

│

├── docs/

│   ├── Project\_Planning.md

│   ├── Project\_Test\_Plan.md

│   ├── Software\_Architecture.md

│   └── Use\_Case\_Model.md

│

└── README.md

```



\## 6. Prerequisites



Install the following before running the application:



\- Python 3.11 or compatible version

\- Node.js and npm

\- PostgreSQL

\- Git



\## 7. Database Setup



1\. Start your PostgreSQL server.

2\. Create a database named `campus\_resource\_management`.

3\. From the project root, execute:



```powershell

psql -U postgres -d campus\_resource\_management -f database/schema.sql

```



4\. Load the initial seed data:



```powershell

psql -U postgres -d campus\_resource\_management -f database/seed.sql

```



Update the database credentials in the backend environment configuration.



\## 8. Backend Setup



Navigate to the backend directory:



```powershell

cd backend

```



Create a virtual environment:



```powershell

python -m venv venv

```



Activate it:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



Install dependencies:



```powershell

pip install -r requirements.txt

```



Create a `.env` file inside the backend directory with the following configuration:



```env

DATABASE\_URL=postgresql://postgres:YOUR\_PASSWORD@localhost:5432/campus\_resource\_management

JWT\_SECRET\_KEY=YOUR\_SECRET\_KEY

```



Replace the placeholders with your own local configuration. Never commit real passwords or secret keys.



Start the backend:



```powershell

python app.py

```



The Flask backend runs at:



`http://localhost:5000`



API health check:



`http://localhost:5000/`



\## 9. Frontend Setup



Open another terminal and navigate to the frontend directory:



```powershell

cd frontend

```



Install dependencies:



```powershell

npm install

```



Start the development server:



```powershell

npm run dev

```



Vite displays the local frontend URL in the terminal.



\## 10. API Modules



The backend exposes the following API modules:



| Module | Base Endpoint

