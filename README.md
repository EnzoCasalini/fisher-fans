# 🎣 Fisher Fans API

Fisher Fans API is a RESTful API designed for managing users, boats, trips, reservations, and logs. It provides endpoints for creating, retrieving, updating, and deleting resources related to fishing activities.

## 📚 Table of Contents

- [✨ Features](#features)
- [⚙️ Installation](#installation)
- [🚀 Usage](#usage)
- [🔗 API Endpoints](#api-endpoints)
- [🤝 Contributing](#contributing)
- [📜 License](#license)

## ✨ Features

- 👤 User management: Create, retrieve, update, and delete users.
- ⛵ Boat management: Manage boats with filtering options.
- 🗺️ Trip management: Organize and manage fishing trips.
- 📅 Reservation management: Handle reservations for trips.
- 📖 Log management: Maintain logs of fishing activities.

## ⚙️ Installation

To set up the project locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/EnzoCasalini/fisher-fans.git
   cd fisher-fans
   ```

2. **Install dependencies:**

   Ensure you have Python and pip installed. Then, run:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**

   Start the FastAPI application using Uvicorn:

   ```bash
   uvicorn app.main:app --reload
   ```

## 🚀 Usage

Once the application is running, you can access the API documentation at `http://localhost:8000/docs` for interactive exploration of the endpoints.

## 🔗 API Endpoints

Here are some of the key endpoints available in the API:

- **Users** 👥

  - `GET /v1/users`: Retrieve a list of users.
  - `POST /v1/users`: Create a new user.
  - `GET /v1/users/{userId}`: Retrieve a user by ID.
  - `PUT /v1/users/{userId}`: Update a user by ID.
  - `DELETE /v1/users/{userId}`: Delete a user by ID.

- **Boats** 🚤

  - `GET /v1/boats`: Retrieve a list of boats.
  - `POST /v1/boats`: Create a new boat.
  - `GET /v1/boats/{boatId}`: Retrieve a boat by ID.
  - `PUT /v1/boats/{boatId}`: Update a boat by ID.
  - `DELETE /v1/boats/{boatId}`: Delete a boat by ID.
  - `GET /v1/boats/bbox`: Retrieve boats within a bounding box.

- **Trips** 🛳️

  - `GET /v1/trips`: Retrieve a list of trips.
  - `POST /v1/trips`: Create a new trip.
  - `GET /v1/trips/{tripId}`: Retrieve a trip by ID.
  - `PUT /v1/trips/{tripId}`: Update a trip by ID.
  - `DELETE /v1/trips/{tripId}`: Delete a trip by ID.

- **Reservations** 📆

  - `GET /v1/reservations`: Retrieve a list of reservations.
  - `POST /v1/reservations`: Create a new reservation.
  - `GET /v1/reservations/{reservationId}`: Retrieve a reservation by ID.
  - `PUT /v1/reservations/{reservationId}`: Update a reservation by ID.
  - `DELETE /v1/reservations/{reservationId}`: Delete a reservation by ID.

- **Logs** 📜
  - `GET /v1/log/{userId}`: Retrieve a user's log.
  - `POST /v1/log/{userId}`: Create a log for a user.
  - `GET /v1/log/{userId}/pages/{page_id}`: Retrieve a page of a user's log.
  - `PUT /v1/log/{userId}/pages/{page_id}`: Update a page of a user's log.
  - `DELETE /v1/log/{userId}/pages/{page_id}`: Delete a page of a user's log.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.