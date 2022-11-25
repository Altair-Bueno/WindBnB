def viviendaEntity(item) -> dict:
    return {
        "id": item["id"],
        "title": item["title"],
        "description": item["description"],
        "user_id": item["user_id"],
        "location": item["location"],
        "state": item["state"],
        "bookings": item["bookings"],
        "url_photo": item["url_photo"],
        "longitude": item["longitude"],
        "latitude": item["latitude"],
        "price": item["price"]
    }
