import random
from zoneinfo import available_timezones

import pytest

from src.api.endpoints.petstore import PetStore

@pytest.fixture
def pet_store():
    return PetStore("https://petstore.swagger.io/v2")

# тест отправляет запрос с минимальным набором полей и проверяет, что объект создался
# поле id также добавлено в тест, так как без него невозможно проверить
# наличие объекта после создания (особенности API)
def test_pet_creation_min_fields(pet_store):

    random_number = random.randint(100,999)
    pet_data = {
        "id":f"{random_number}",
        "name": f"test_pet_{random_number}",
        "photoUrls": ["string"]
    }

    response = pet_store.create_pet(pet_data)
    pet_id = response.json()["id"]
    print(f"pet {pet_id} {response.json()}")

    assert response.status_code == 200
    assert response.json()["id"] == int(pet_data["id"])
    assert response.json()["name"] == pet_data["name"]

    get_response = pet_store.get_pet(pet_id)
    assert get_response.status_code == 200
    assert get_response.json()["id"] == int(pet_data["id"])
    assert get_response.json()["name"] == pet_data["name"]


# тест отправляет запрос с максимальным набором полей и проверяет, что объект создался
@pytest.mark.parametrize("state", ["available", "pending", "sold"])
def test_pet_creation_max_fields(pet_store, state):

    random_number = random.randint(100,999)
    pet_data = {
            "id": random_number,
            "category": {
                "id": random_number,
                "name": f"test_pet_{random_number}"
            },
            "name": f"test_pet_{random_number}",
            "photoUrls": [
                "string"
            ],
            "tags": [
                {
                    "id": random_number,
                    "name": f"test_pet_{random_number}"
                }
            ],
            "status": state
        }


    response = pet_store.create_pet(pet_data)
    pet_id = response.json()["id"]
    print(f"pet {pet_id} {response.json()}")

    assert response.status_code == 200

    get_response = pet_store.get_pet(pet_id)
    assert get_response.status_code == 200
    assert get_response.json()["id"] == int(pet_data["id"])


# тест проверяет, что при создании сущности с дублирующимся
# id происходин обновление существующей записи
def test_pet_creation_duplicate_id(pet_store):
    random_number = random.randint(100, 999)
    pet_data = {
        "id": f"{random_number}",
        "name": f"test_pet_{random_number}",
        "photoUrls": ["string"]
    }

    response = pet_store.create_pet(pet_data)
    pet_id = response.json()["id"]
    print(f"pet {pet_id} {response.json()}")

    assert response.status_code == 200
    assert pet_id == int(pet_data["id"])
    assert response.json()["name"] == pet_data["name"]

    get_response = pet_store.get_pet(pet_id)
    assert get_response.status_code == 200
    assert pet_id == int(pet_data["id"])
    assert get_response.json()["name"] == pet_data["name"]

    pet_data_duplicate_id = {
        "id": f"{pet_id}",
        "name": f"test_pet_duplicate_id_{random_number}",
        "photoUrls": ["string"]
    }

    response_duplicate_id = pet_store.create_pet(pet_data_duplicate_id)

    print(f"pet {pet_id} {response_duplicate_id.json()}")
    assert response_duplicate_id.status_code == 200
    assert pet_id == int(pet_data["id"])
    assert response_duplicate_id.json()["name"] == pet_data_duplicate_id["name"]

    get_response = pet_store.get_pet(pet_id)
    assert get_response.status_code == 200
    assert pet_id == int(pet_data["id"])
    assert get_response.json()["name"] == pet_data_duplicate_id["name"]