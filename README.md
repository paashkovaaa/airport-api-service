## Airport API Service✈️

This project is an Airport API Service built with Django and Docker, providing RESTful APIs for managing various entities such as Crew, Countries, Cities, Airports, Airplane Types, Airplanes, Routes, Flights, Users, Orders.

## Running with Docker

To run the project with Docker, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/paashkovaaa/airport-api-service.git
    ```

2. Navigate to the project directory:

    ```bash
    cd airport-api-service
    ```

3. Build and run the Docker containers:

    ```bash
    docker-compose up --build
    ```

4. Access the API endpoints via `http://localhost:8000/`.

## Running on Machine

To run the project on your local machine without Docker, follow these steps:

1. Ensure you have Python installed (preferably version 3.7 or later).

2. Clone the repository:

    ```bash
    git clone https://github.com/paashkovaaa/airport-api-service.git
    ```

3. Navigate to the project directory:

    ```bash
    cd airport-api-service
    ```

4. Install the Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

7. Access the API endpoints via `http://localhost:8000/`.

## Swagger Documentation:
  - `/api/doc/swagger/`
    - Provides the Swagger UI interface for interactive documentation of the API endpoints. Developers can explore and test the endpoints directly from the browser.

- **Redoc Documentation**:
  - `/api/doc/redoc/`
    - Offers the Redoc interface for API documentation, providing an alternative layout and styling for viewing and interacting with the API documentation.


## API Endpoints

Below is a summary of the API endpoints provided by the project:

- **Crews**: `/api/airport/crews/`
- **Countries**: `/api/airport/countries/`
- **Cities**: `/api/airport/cities/`
- **Airports**: `/api/airport/airports/`
- **Airplane Types**: `/api/airport/airplane_types/`
- **Airplanes**: `/api/airport/airplanes/`
- **Routes**: `/api/airport/routes/`
- **Flights**: `/api/airport/flights/`
- **Orders**: `/api/airport/orders/`
- **Users**: `/api/user/register`,`/api/user/me` `/api/user/token`, `/api/user/token/refresh`, `/api/user/token/verify`

Each endpoint supports various operations such as listing, creation, retrieval, and updating of resources.
