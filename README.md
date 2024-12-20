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
- **Python 3.x**: Programming language used.

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

### Authentication

- **Obtain a JWT token**:
    ```sh
    POST /api/token/
    ```

    **Request Body**:
    ```json
    {
      "username": "your_username",
      "password": "your_password"
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

### Booking

- **Create a booking**:
    ```sh
    POST /booking/
    ```

    **Request Body**:
    ```json
    {
      "room": "room_id",
      "check_in_date": "YYYY-MM-DD",
      "check_out_date": "YYYY-MM-DD"
    }
    ```

    **Response**:
    ```json
    {
        {
        "detail": "detail",
        "code": "code",
        "error": null,
        "data": {
            "message": "message",
            "booking_id": "id number"
            }
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

To test the API using Postman, [download the Postman collection here](path/to/your-postman-collection.json) and import it into Postman. Once imported, you can run all the requests and view the responses.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
