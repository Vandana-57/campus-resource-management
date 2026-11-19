def resource_to_dict(resource):
    return {
        "resource_id": resource.resource_id,
        "resource_name": resource.resource_name,
        "resource_type": resource.resource_type,
        "location": resource.location,
        "description": resource.description,
        "is_active": resource.is_active
    }


def booking_to_dict(booking):
    return {
        "booking_id": booking.booking_id,
        "user_id": booking.user_id,
        "resource_id": booking.resource_id,
        "booking_date": str(booking.booking_date),
        "start_time": str(booking.start_time),
        "end_time": str(booking.end_time),
        "status": booking.status,
        "created_at": str(booking.created_at)
    }


def incident_to_dict(incident):
    return {
        "incident_id": incident.incident_id,
        "user_id": incident.user_id,
        "resource_id": incident.resource_id,
        "title": incident.title,
        "description": incident.description,
        "status": incident.status,
        "created_at": str(incident.created_at)
    }
