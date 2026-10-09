# Cloud Native Car Rental Service

[![CI](https://github.com/Artmis137/cloud-native-rental-service/actions/workflows/ci.yml/badge.svg)](https://github.com/Artmis137/cloud-native-rental-service/actions/workflows/ci.yml)

REST API for a car rental service, built with FastAPI.
This project is a Python adaptation of a Java / Spring Boot assignment from the Cloud Native course (MLSD M1).

## From Spring Boot to FastAPI

The course presents these concepts with Spring Boot. Here is how each one maps to this implementation:

| Spring Boot | FastAPI (this project) |
|---|---|
| `@RestController` + `@RequestMapping("/cars")` | `APIRouter(prefix="/cars")` in `app/api/cars.py` |
| `@GetMapping` / `@PutMapping` | `@router.get` / `@router.put` |
| `@PathVariable` | Path parameter (`plateNumber: str`) |
| `@RequestParam` | `Query(...)` (`rent: bool`) |
| `@RequestBody` | `Body(...)` with a Pydantic model (`Dates`) |
| Bean Validation (`@Valid`, constraints) | Pydantic v2 models and `model_validator` |
| `ResponseStatusException` | `HTTPException` (404, 400) |
| `SpringApplication` + embedded Tomcat | `FastAPI()` app served by Uvicorn |
| Maven / Gradle | uv (`pyproject.toml`, `uv.lock`) |
| `MockMvc` / `TestRestTemplate` | pytest with FastAPI `TestClient` |

## Tech stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Data validation:** [Pydantic v2](https://docs.pydantic.dev/)
- **ASGI server:** [Uvicorn](https://www.uvicorn.org/)
- **Package manager:** [uv](https://docs.astral.sh/uv/)
- **Tests:** pytest
- **Containerization:** Docker
- **CI:** GitHub Actions
- **Python:** 3.12+

## Project structure

```
.
├── app/
│   ├── main.py          # FastAPI application entry point
│   ├── api/
│   │   └── cars.py      # /cars endpoints
│   └── schemas/
│       └── car.py       # Pydantic models (CarBase, Dates)
├── tests/               # API tests (pytest)
├── .github/workflows/   # CI pipeline (tests + Docker build)
├── Dockerfile
├── pyproject.toml
└── uv.lock
```

## Getting started

1. **Clone the repository**

   ```bash
   git clone https://github.com/Artmis137/cloud-native-rental-service.git
   cd cloud-native-rental-service
   ```

2. **Install the dependencies**

   ```bash
   uv sync
   ```

3. **Run the development server**

   ```bash
   uv run uvicorn app.main:app --reload
   ```

4. **Open the API**

   - API root: <http://localhost:8000/>
   - Swagger UI: <http://localhost:8000/docs>
   - ReDoc: <http://localhost:8000/redoc>

## Run with Docker

```bash
docker build -t car-rental-api .
docker run -p 8000:8000 car-rental-api
```

The API is then available at <http://localhost:8000/docs>.

## Tests

```bash
uv run pytest -v
```

The CI pipeline runs the test suite on every push and pull request, then builds the Docker image and checks that the container answers.

## API endpoints

| Method | Endpoint               | Description                              |
|--------|------------------------|------------------------------------------|
| GET    | `/`                    | Health check                             |
| GET    | `/cars`                | List the cars that are not rented        |
| GET    | `/cars/{plateNumber}`  | Get the details of a car                 |
| PUT    | `/cars/{plateNumber}`  | Rent (`rent=true`) or return (`rent=false`) a car |

### Examples

List the available cars:

```bash
curl http://localhost:8000/cars
```

Rent a car for a given period:

```bash
curl -X PUT "http://localhost:8000/cars/11AA22?rent=true" \
     -H "Content-Type: application/json" \
     -d '{"begin": "2026-01-01", "end": "2026-01-05"}'
```

Return a car:

```bash
curl -X PUT "http://localhost:8000/cars/11AA22?rent=false"
```

### Error responses

| Status | Reason                                                       |
|--------|--------------------------------------------------------------|
| 400    | The car is already rented, or returned while not rented      |
| 404    | No car matches the given plate number                        |
| 422    | Invalid input (e.g. bad date format, end date before begin)  |

## Notes

Data is stored in memory: every change is lost when the server restarts.

## Author

Mamadou NIMAGA