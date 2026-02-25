import random
import time

import allure
import pytest

from src.utils.json_helpers import find_text

@pytest.mark.smoke
@allure.title("Создание питомца с минимальными полями")
@allure.feature("Питомцы")
@allure.severity(allure.severity_level.CRITICAL)
def test_pet_creation_min_fields(pet_store, base_pet_data, create_base_pet):
    """Создание с id, name, photoUrls + проверка через GET"""

    with allure.step("1. Создание питомца"):
        created_pet = create_base_pet.json()
        assert create_base_pet.status_code == 200
        assert created_pet["id"] == int(base_pet_data["id"])
        assert created_pet["name"] == base_pet_data["name"]

        allure.attach(
            f"Status created_pet: {create_base_pet.status_code}, \nBody: {created_pet}",
            name="created_pet response",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("2. Получение созданного питомца"):
        get_response = pet_store.get_pet(created_pet["id"])
        get_pet = get_response.json()
        assert get_response.status_code == 200
        assert get_pet["id"] == int(base_pet_data["id"])
        assert get_pet["name"] == base_pet_data["name"]

        allure.attach(
            f"Status get_pet: {get_response.status_code}, \nBody: {get_pet}",
            name="get_pet response",
            attachment_type=allure.attachment_type.TEXT
        )


@pytest.mark.parametrize("state", ["available", "pending", "sold"])
def test_pet_creation_max_fields(pet_store, full_pet_data, create_full_pet, state):
    """
    Тест отправляет запрос с максимальным набором полей и проверяет,
    что объект создался для каждого из статусов.
    Ожидаемый результат 200.
    """
    assert create_full_pet.status_code == 200

    get_response = pet_store.get_pet(create_full_pet.json()["id"])
    assert get_response.status_code == 200
    assert get_response.json()["id"] == int(full_pet_data["id"])
    ###CHECK ALL FIELDS



def test_pet_creation_duplicate_id(pet_store):
    """
    Тест проверяет, что при создании сущности с дублирующимся
    id происходит обновление существующей записи
    """

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


#тест проверяет работу put-запроса для редактирования имеющейся записи
def test_edit_pet(pet_store):
    random_number = random.randint(100, 999)
    pet_data = {
        "id": random_number,
        "name": f"test_pet_{random_number}",
    }

    pet_store.create_pet(pet_data)

    pet_data["name"] = f"test_pet_put_{random_number}"
    response = pet_store.edit_pet(pet_data)

    assert response.status_code == 200
    assert response.json()["id"] == pet_data["id"]
    assert response.json()["name"] == pet_data["name"]


#тест позволяет получить информаци по id
def test_get_pet(pet_store):
    random_number = random.randint(100, 999)
    pet_data = {
        "id": random_number,
        "name": f"test_pet_{random_number}",
    }
    response = pet_store.create_pet(pet_data)
    pet_store.get_pet(pet_data["id"])

    assert response.status_code == 200
    assert response.json()["id"] == pet_data["id"]
    assert response.json()["name"] == pet_data["name"]

#тест показывает: если с таким id записи нет,то сервер вернет ошибку 404
def test_get_pet_absent(pet_store):
    pet_id = int(time.time())

    response = pet_store.get_pet(pet_id)

    assert response.status_code == 404, (
        f"Ожидался код 404 для несуществующего питомца {pet_id}, "
        f"получен {response.status_code}"
    )
