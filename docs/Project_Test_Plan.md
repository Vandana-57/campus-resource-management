# Project Test Plan
## Campus Resource Management System

### 1. Objective
Verify the correctness, security and reliability of the Campus Resource Management System.

### 2. Testing Scope
- Registration and login
- User authentication
- Resource retrieval
- Booking creation
- Booking history
- Booking cancellation
- Administrator operations
- Incident management
- Notifications

### 3. Testing Approach
- Unit testing
- API testing
- Integration testing
- Authentication and authorization testing
- Frontend build verification

### 4. Test Environment
Python 3.11, Flask, PostgreSQL, Pytest, React and Vite.

### 5. Test Cases
| ID | Test scenario | Expected result |
| TC01 | Valid registration | Account created |
| TC02 | Duplicate registration | Error returned |
| TC03 | Valid login | JWT token returned |
| TC04 | Invalid login | Authentication rejected |
| TC05 | View profile | Authenticated profile returned |
| TC06 | List resources | Active resources returned |
| TC07 | Create valid booking | Booking created |
| TC08 | Overlapping booking | Conflict rejected |
| TC09 | View booking history | User bookings returned |
| TC10 | Cancel own booking | Booking cancelled |
| TC11 | Unauthorized access | Access rejected |
| TC12 | Admin operations | Role permissions enforced |
| TC13 | Incident operations | Valid incident response |
| TC14 | Notifications | Correct notification response |

### 6. Existing Test Evidence
A previous execution reported 24 out of 24 backend tests passing. Re-run the tests before final submission and attach the terminal screenshot as evidence.

### 7. Acceptance Criteria
- Backend tests pass.
- API responds correctly.
- Database connection works.
- Unauthorized access is rejected.
- Frontend production build succeeds.
- Main user workflows are demonstrated.
