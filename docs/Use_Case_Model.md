# Use Case Model
## Campus Resource Management System

```mermaid
flowchart TB
    Student([Student])
    Faculty([Faculty])
    Admin([Administrator])

    subgraph System[Campus Resource Management System]
        UC1((Register / Login))
        UC2((View Resources))
        UC3((Book Resources))
        UC4((View Booking History))
        UC5((Cancel Booking))
        UC6((Manage Resources))
        UC7((Manage Bookings))
        UC8((Manage Incidents))
        UC9((View Notifications))
    end

    Student --> UC1
    Student --> UC2
    Student --> UC3
    Student --> UC4
    Student --> UC5
    Student --> UC9

    Faculty --> UC1
    Faculty --> UC2
    Faculty --> UC3
    Faculty --> UC4
    Faculty --> UC9

    Admin --> UC1
    Admin --> UC6
    Admin --> UC7
    Admin --> UC8
    Admin --> UC9
    Admin --> UC2
        UC8 --> Admin
        UC9 --> Admin
    end
        UC8 --> Admin
        UC9 --> Admin
    end
    Admin --> UC6
    Admin --> UC7
    Admin --> UC8
    Admin --> UC9
    Admin --> UC2

