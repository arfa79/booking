# Booking API

This project is a Django-based API for booking hotel rooms. It provides endpoints for user authentication and room booking.

## Features

- User authentication using JWT tokens
- Room booking with date validation and conflict checking
- Custom responses for API endpoints
- Logging for debugging and monitoring

## Technologies Used

- **Django**: Web framework for building the API.
- **Django REST Framework**: For creating RESTful API endpoints.
- **JWT Authentication**: For secure user authentication.
- **PostgreSQL**: Database used for storing data (you can modify it in the `.env` file).
- **Python**: Programming language used.

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/arfa79/booking.git
    cd booking
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a `.env` file in the root directory and add the following variables:
    ```env
    SECRET_KEY=<your-secret-key>
    DEBUG=True
    DATABASE_URL=postgres://username:password@localhost/dbname
    ```

5. **Apply migrations**:
    ```sh
    python manage.py migrate
    ```

6. **Create a superuser**:
    ```sh
    python manage.py createsuperuser
    ```

7. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

    The development server will be running at `http://127.0.0.1:8000`.

## Usage

### Django Shell Usage For Database Data Injection

To create initial data for your application, you can use the Django shell.

1. **Open Django Shell**  
   Run the following command in your terminal:
   ```sh
   python manage.py shell
   ```
2. **Import the Necessary Models**
   Use these imports to access your models and the Django User model: 
   ```python
   from core.models import Hotel, Room
   from django.contrib.auth.models import User
   ```
3. **Create a Hotel Object**
   Replace "Grand Plaza Hotel" and "New York City" with your desired hotel name and location: 
   ```python
   hotel = Hotel.objects.create(name="Grand Plaza Hotel", location="New York City")
   ```
4. **Create Room Objects**
   Use the Room model to create rooms associated with the hotel. Replace room numbers as needed: 
   ```python
   room1 = Room.objects.create(hotel=hotel, room_number="101")
   room2 = Room.objects.create(hotel=hotel, room_number="102")
   ```
5. **Create a User**
   Replace "testuser" and "password123" with the username and password you want to use: 
   ```python
   user = User.objects.create_user(username="testuser", password="password123")
   ```
6. **Print the IDs**
   Print the IDs of the created objects to confirm successful creation: 
   ```python
   print(f"Hotel ID: {hotel.id}, Room1 ID: {room1.id}, Room2 ID: {room2.id}, User ID: {user.id}")
   ```

### Authentication Examples

- **Obtain a JWT token**:
    ```sh
    POST /api/token/
    ```

    **Request Body**:
    ```json
    {
      "username": "alireza",
      "password": "123"
    }
    ```

    **Response**:
    ```json
    {
      "access": "your-access-token",
      "refresh": "your-refresh-token"
    }
    ```

- **Refresh a JWT token**:
    ```sh
    POST /api/token/refresh/
    ```

    **Request Body**:
    ```json
    {
      "refresh": "your-refresh-token"
    }
    ```

### Booking Examples

- **Create a booking**:
    ```sh
    POST /booking/
    ```

    **Request Body**:
    ```json
    {
        "room": 1,
        "start_at": "2026-06-01T12:00:00",
        "end_at": "2026-06-01T14:00:00"
    }
    ```

    **Response**:
    ```json
    {
        "detail": "Success",
        "code": "success",
        "error": null,
        "data": {
            "message": "Booking successful!",
            "booking_id": 1
        }
    }
    ```

### Admin

Access the Django admin interface at `/admin/` to manage hotels, rooms, and bookings.

## Running Tests

To run the tests, use the following command:
    ```sh
    python manage.py test
    ```

## Postman Examples

Below are examples of using Postman to interact with the API:

### 1. Obtain JWT Token

**POST** `/api/token/`

![JWT Token Request](assets/screenshots/jwt-token-request.png)

**Response**:

![JWT Token Response](assets/screenshots/jwt-token-response.png)

---

### 2. Create a Booking

**POST** `/booking/`

![Create Booking Request](assets/screenshots/create-booking-request.png)

**Response**:

![Create Booking Response](assets/screenshots/create-booking-response.png)

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
