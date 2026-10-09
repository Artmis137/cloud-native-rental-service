# Cloud Native Car Rental Service

REST API for a car rental service, built with FastAPI.
This project is a Python adaptation of a Java / Spring Boot assignment from the Cloud Native course (MLSD M1).

## Tech stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Data validation:** [Pydantic v2](https://docs.pydantic.dev/)
- **ASGI server:** [Uvicorn](https://www.uvicorn.org/)
- **Package manager:** [uv](https://docs.astral.sh/uv/)
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
