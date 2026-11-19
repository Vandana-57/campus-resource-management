# Campus Resource Management System
## Software Architecture Document

### 1. Overview
The Campus Resource Management System provides a centralized platform for managing campus resources and student bookings.

### 2. Technology Stack
- Frontend: React.js, Vite, JavaScript, React Router
- Backend: Python Flask
- Database: PostgreSQL
- ORM: SQLAlchemy
- Authentication: JWT
- API communication: Axios and REST APIs

### 3. Architecture
The system follows a three-tier architecture.

1. Presentation Layer: React frontend, pages, components and authentication context.
2. Application Layer: Flask REST API, route blueprints, validation and business logic.
3. Data Layer: PostgreSQL database accessed through SQLAlchemy models.

### 4. Main Modules
- User registration and login
- User profile and authentication
- Campus resource listing
- Resource booking and booking history
- Booking cancellation
- Administrator management
- Incident management
- Notifications

### 5. API Endpoints
| Method | Endpoint | Purpose |
| POST | /api/auth/register | Register user |
| POST | /api/auth/login | Authenticate user |
| GET | /api/auth/profile | Get authenticated profile |
| GET | /api/resources | List active resources |
| POST | /api/bookings/ | Create booking |
| GET | /api/bookings/my | View booking history |
| DELETE | /api/bookings/{booking_id} | Cancel booking |
| / | /api/admin/* | Administration APIs |
| / | /api/notifications/* | Notification APIs |

Incident APIs are registered under /api.

### 6. Security
- JWT-based protected API routes
- Password hashing
- Role-based route protection
- Input validation
- Booking ownership checks
- CORS configuration

### 7. Database
PostgreSQL stores users, resources, bookings and other system records. SQLAlchemy provides database access.

### 8. Data Flow
User -> React Interface -> REST API -> Flask Routes -> SQLAlchemy -> PostgreSQL.
The response returns through the API to the React interface.

### 9. Deployment
The frontend is developed using Vite and the backend runs using Flask. Production deployment configuration must be completed separately.
