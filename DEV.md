# Development Guidelines

## Project Structure
- **app.py**: Main FastAPI application.
- **logic.py**: Contains core validation logic.
- **config/**: Configuration files (YAML format).

## Key Dependencies
- `FastAPI`: Web framework for building APIs.
- `Pydantic`: Data validation and settings management.
- `Dynaconf`: Configuration management.

## Running in Development Mode
- **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
- **Run the Server**:
    ```bash
    uvicorn app:app --reload
    ```

## Modifying Schema or Settings
- Modify `config/schema.yaml` or `config/settings.yaml` as needed.
- Testing Changes: Restart the server to apply changes.

## Docker Workflow
- **Building the Image**:
    ```bash
    docker build -t strata-fit-data-val .
    ```
- **Running the Container**: Ensure the `config/` directory is correctly mounted:
    ```bash
    docker run --rm -p 8000:8000 -v $(pwd)/config:/app/config strata-fit-data-val
    ```

## Versioning
- Ensure the correct version of each dependency is specified in `requirements.txt`.
- The version of the app is managed in `config/settings.yaml` under `openapi.version`.

## CI/CD with GitHub Actions
- Configuration for building and pushing Docker images is in `.github/workflows/docker-image.yml`.