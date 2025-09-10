def test_service1_alive():
    # умовно: тут може бути реальний healthcheck запит до API
    service_status = True
    assert service_status, "Service 1 is not alive"


def test_service2_alive():
    service_status = False  # приклад помилки
    assert service_status, "Service 2 is not alive"
