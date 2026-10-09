RENTAL_DATES = {"begin": "2026-01-01", "end": "2026-01-05"}


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello world!"


def test_list_cars_returns_only_available_cars(client):
    response = client.get("/cars")
    assert response.status_code == 200
    plates = [car["plateNumber"] for car in response.json()]
    assert plates == ["11AA22", "CC22DD"]


def test_get_car(client):
    response = client.get("/cars/AA11BB")
    assert response.status_code == 200
    assert response.json()["brand"] == "Renault"


def test_get_unknown_car_returns_404(client):
    assert client.get("/cars/UNKNOWN").status_code == 404


def test_rent_car_with_dates(client):
    response = client.put("/cars/11AA22?rent=true", json=RENTAL_DATES)
    assert response.status_code == 200
    assert "from 2026-01-01 to 2026-01-05" in response.json()["message"]
    assert client.get("/cars/11AA22").json()["is_rented"] is True


def test_rented_car_is_no_longer_listed(client):
    client.put("/cars/11AA22?rent=true")
    plates = [car["plateNumber"] for car in client.get("/cars").json()]
    assert "11AA22" not in plates


def test_rent_already_rented_car_returns_400(client):
    assert client.put("/cars/AA11BB?rent=true").status_code == 400


def test_return_car(client):
    response = client.put("/cars/AA11BB?rent=false")
    assert response.status_code == 200
    assert client.get("/cars/AA11BB").json()["is_rented"] is False


def test_return_car_not_rented_returns_400(client):
    assert client.put("/cars/11AA22?rent=false").status_code == 400


def test_update_unknown_car_returns_404(client):
    assert client.put("/cars/UNKNOWN?rent=true").status_code == 404


def test_rent_with_end_before_begin_returns_422(client):
    dates = {"begin": "2026-01-05", "end": "2026-01-01"}
    assert client.put("/cars/11AA22?rent=true", json=dates).status_code == 422


def test_rent_with_invalid_date_format_returns_422(client):
    dates = {"begin": "01/01/2026", "end": "2026-01-05"}
    assert client.put("/cars/11AA22?rent=true", json=dates).status_code == 422
