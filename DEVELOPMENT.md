# Local Development Setup

This guide provides instructions for setting up and running the application locally using Docker for the PostgreSQL database.

## Prerequisites

*   **Docker**: Ensure Docker is installed and running on your system. Download from [https://www.docker.com/get-started](https://www.docker.com/get-started).
*   **Docker Compose**: Ensure Docker Compose is installed. It's typically included with Docker Desktop. If not, follow instructions at [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/).
*   **Python**: Ensure Python 3.7+ is installed.
*   **Poetry** (or pip): This project uses Poetry for dependency management (adjust if using pip directly with requirements.txt). `pip install poetry`.

## Setup and Running

1.  **Clone the Repository** (if you haven't already):
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Install Python Dependencies**:
    If using Poetry:
    ```bash
    poetry install
    ```
    If using pip and `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
    *(The worker has been using `pip freeze > requirements.txt`, so pip instructions are appropriate)*

3.  **Start the PostgreSQL Database**:
    This command will start a PostgreSQL container in detached mode and build the image if it doesn't exist.
    ```bash
    docker-compose up -d --build db
    ```
    *   The database will be running on `localhost:5432`.
    *   Credentials (defined in `docker-compose.yml` and `app/core/config.py`):
        *   **Username**: `myuser`
        *   **Password**: `mypass`
        *   **Database Name**: `myappdb`
    *   Data is persisted in a local volume named `.postgres-data/` in your project root.

4.  **Run Database Migrations**:
    Once the database container is running, apply the latest database schema migrations using Alembic.
    (Ensure your Alembic CLI is accessible. If installed in a virtual environment, activate it first.)
    ```bash
    alembic upgrade head
    ```
    *(Note: If alembic is installed via poetry or globally, this command might be `poetry run alembic upgrade head` or just `alembic upgrade head`)*

5.  **Seed the Database with Fake Data** (Optional):
    To populate the database with initial fake data (e.g., users), run the seeding script:
    ```bash
    python scripts/seed_db.py
    ```
    *(If using poetry: `poetry run python scripts/seed_db.py`)*

6.  **Run the Application**:
    (Instructions for running the main application, e.g., using Uvicorn for a FastAPI app)
    ```bash
    # Example for a FastAPI app in main.py, app instance named 'app'
    uvicorn main:app --reload
    ```
    *(This part is an example, the user should fill in their specific run command if different)*

## Stopping the Database

To stop the PostgreSQL container:
```bash
docker-compose down
```
This will stop the container but preserve the data in the `./.postgres-data/` volume. To remove the volume and all data, you can run `docker-compose down -v`.

## Connecting to the Database Locally

You can connect to the PostgreSQL database using any standard SQL client (e.g., DBeaver, pgAdmin, psql) with the following details:
*   **Host**: `localhost`
*   **Port**: `5432`
*   **Username**: `myuser`
*   **Password**: `mypass`
*   **Database Name**: `myappdb`
