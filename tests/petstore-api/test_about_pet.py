import random

import pytest

from src.api.endpoints.petstore import PetStore
from src.utils.json_helpers import find_text

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
# id происходит обновление существующей записи
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


#тест проверяет получение списка питомцев с конкретным статусом
@pytest.mark.parametrize("state", ["available", "pending", "sold"])
def test_get_pets_by_status(pet_store, state):

        random_number = random.randint(100, 999)
        pet_data = {
            "id": random_number,
            "name": f"test_pet_{random_number}",
            "status": state
        }

        response = pet_store.create_pet(pet_data)
        pet_id = response.json()["id"]
        print(f"pet {pet_id} {response.json()}")

        assert response.status_code == 200

        pets_by_status_response = pet_store.get_pet_by_state(state)
        pets_by_status_json = pet_store.get_pet_by_state(state).json()

        # Комбинация полей для поиска
        found_pet = find_text(
            pets_by_status_json,
            id=pet_data["id"],
            name=pet_data["name"],
            status=state
        )

        assert found_pet is not None, f"Питомец не найден в статусе {state}"
        assert found_pet["id"] == pet_data["id"]
        assert found_pet["name"] == pet_data["name"]
        assert found_pet["status"] == state
        assert pets_by_status_response.status_code == 200