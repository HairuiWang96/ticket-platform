# Ticket Support Platform (Code Challenge)

## Overview

The Ticket Support Platform is a web application built with React that allows users to view, create, update, and manage tickets for customer support purposes.

## Setup Instructions

### Running with Docker

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/HairuiWang96/ticket-platform
    ```

2. **Build and Run Docker Containers**:

    ```bash
    cd ticket-support-platform
    docker-compose up --build
    ```

3. **Access the Application**:
   Open your web browser and navigate to `http://localhost:5173` to access the application.

## Explanation

### Components

-   **TicketList**: Displays a list of tickets fetched from the API. Users can click on a ticket to view its details.
-   **TicketDetails**: Shows detailed information about a specific ticket, including its subject, status, assignee, priority, and description. Users can also navigate to view the thread associated with the ticket or edit the ticket.
-   **TicketUpdateForm**: Allows users to update the status, assignee, and priority of a ticket.

### API Integration

-   The application communicates with the backend API to fetch and update ticket data. It uses `apiService` for making API requests.

## Backend Setup Instructions

### Prerequisites

-   Python (3.7+)
-   SQLAlchemy
-   FastAPI
-   Nylas SDK
-   PostgreSQL (or any other supported database)

### Running the Backend Locally

1. **Clone the Backend Repository**:

    ```bash
    git clone https://github.com/HairuiWang96/ticket-platform-backend
    ```

2. **Install Dependencies**:

    ```bash
    cd ticket-platform-backend
    pip install -r requirements.txt
    ```

3. **Set up Environment Variables**:

    - Create a `.env` file in the root directory of the backend repository.
    - Refer to .env.example

4. **Run the Backend Server**:

    ```bash
    uvicorn main:app --reload
    ```

5. **Access the Backend API**:
   Open your web browser and navigate to `http://localhost:8000` to access the backend API documentation.

## Assumptions Made

-   The backend API provides endpoints for fetching ticket data (`GET /tickets`) and updating ticket data (`PUT /tickets/{ticket_id}`).
-   Each ticket has a unique identifier (`id`) and contains information such as subject, status, assignee, priority, and description.
-   The application is styled using Material-UI components and follows a responsive design approach.

## Technologies Used

-   React
-   React Router DOM
-   Material-UI
-   FastAPI
-   SQLAlchemy
-   Nylas SDK
