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
    """
    Создание с id, name, photoUrls + проверка через GET
    Swagger: POST /pet Add a new pet to the store
    """

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


@pytest.mark.smoke
@allure.title("Создание питомца со всеми полями и разными статусами")
@allure.feature("Питомцы")
@allure.severity(allure.severity_level.NORMAL)

@pytest.mark.parametrize("status", ["available", "pending", "sold"])
def test_pet_creation_max_fields(pet_store, all_pet_data_no_state, create_full_pet, status):
    """
    Создание с максимальным набором полей и проверка
    через GET для каждого из статусов.
    Swagger: POST /pet Add a new pet to the store
    """

    allure.dynamic.title(f"Тест создания питомца со статусом: {status}")
    allure.dynamic.description("Проверка POST запроса и последующего GET запроса на соответствие полей")

    with allure.step("1. Создание питомца"):
        assert create_full_pet.status_code == 200
        created_pet = create_full_pet.json()

        allure.attach(
            f"Status created_pet: {create_full_pet.status_code}, \nBody: {created_pet}",
            name="created_pet response",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("2. Получение питомца из БД"):
        get_pet_from_api = pet_store.get_pet(create_full_pet.json()["id"])
        actual_pet = get_pet_from_api.json()
        assert get_pet_from_api.status_code == 200

        allure.attach(
            f"Status get_pet: {get_pet_from_api.status_code}, \nBody: {actual_pet}",
            name="get_pet response",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("3. Сравнение созданного питомца и полученного из БД"):
        assert actual_pet == created_pet

        allure.attach(
            f"Pet from DB:\n{actual_pet}\n\nCreated pet:\n{created_pet}",
            name="comparison_data",
            attachment_type=allure.attachment_type.TEXT
        )


@pytest.mark.smoke
@allure.title("Обновление питомца с данными формы")
@allure.feature("Питомцы")
@allure.severity(allure.severity_level.NORMAL)

def test_pet_update_form_data(pet_store, base_pet_data, create_base_pet):
    """
    Обновление по id и проверка через GET
    Swagger: /pet/{pet_id} Updates a pet in the store with form data
    """

    with allure.step("1. Создание питомца"):
        created_pet = create_base_pet.json()
        pet_id = created_pet["id"]

        assert create_base_pet.status_code == 200

        allure.attach(
            f"Status created_pet: {create_base_pet.status_code}, \nBody: {created_pet}",
            name="created_pet response",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("2. Обновление питомца"):
        updated_pet = pet_store.update_pet_form_data(pet_id, name=f"{pet_id}_updated", status="sold")
        assert updated_pet.status_code == 200

        allure.attach(
            f"Status updated_pet: {updated_pet.status_code}, \nBody: {updated_pet.json()}",
            name="updated_pet response",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("3. Получение питомца из БД"):
        get_pet_from_api = pet_store.get_pet(pet_id)
        actual_pet = get_pet_from_api.json()
        assert get_pet_from_api.status_code == 200

        allure.attach(
            f"Status get_pet: {get_pet_from_api.status_code}, \nBody: {actual_pet}",
            name="get_pet response",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("4. Проверка, что поля обновлены"):
        assert actual_pet["id"] == pet_id
        assert actual_pet["name"] == f"{pet_id}_updated"
        assert actual_pet["status"] == "sold"

        allure.attach(
            f"Pet from DB:\n{actual_pet}\n\nCreated pet:\n{created_pet}\nUpdated pet:\n{updated_pet.json()}",
            name="comparison_data",
            attachment_type=allure.attachment_type.TEXT
        )


@pytest.mark.smoke
@allure.title("Получение списка питомцев с конкретным статусом")
@allure.feature("Питомцы")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("status", ["available", "pending", "sold"])
def test_get_pets_by_status(pet_store, all_pet_data_no_state, create_full_pet, status):
    """
    Получение списка питомцев с конкретным статусом
    Swagger: /pet/findByStatus Finds Pets by status
    """

    with allure.step(f"1. Создание питомца со статусом {status}"):
        created_pet = create_full_pet.json()
        pet_id = created_pet["id"]
        pet_name = created_pet["name"]

        assert create_full_pet.status_code == 200

        allure.attach(
            f"Status created_pet: {create_full_pet.status_code}, \nBody: {created_pet}",
            name="created_pet response",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step(f"2. Получение из базы всех питомцев со статусом {status}"):

        pets_by_status_response = pet_store.get_pet_by_status(status)
        pets_by_status_json = pets_by_status_response.json()

        assert pets_by_status_response.status_code == 200

        allure.attach(
            f"Finds Pets by status response: {pets_by_status_response.status_code}, \nBody: {pets_by_status_json}",
            name=f"pet with status {status} response",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step(f"3. Поиск созданного питомца со статусом {status} в ответе от БД"):
        # Комбинация полей для поиска
        found_pet = find_text(
            pets_by_status_json,
            id=pet_id,
            name=pet_name,
            status=status
        )

        allure.attach(
            f"Expected id {pet_id}\nExpected name: {pet_name}\nFound Object: {found_pet}",
            name=f"Search Result",
            attachment_type=allure.attachment_type.TEXT
        )

        assert found_pet is not None, f"Питомец не найден в статусе {status}"
        assert found_pet["id"] == pet_id
        assert found_pet["name"] == pet_name
        assert found_pet["status"] == status


@pytest.mark.smoke
@allure.title("Обновление имеющейся записи с помощью PUT и проверка через GET")
@allure.feature("Питомцы")
@allure.severity(allure.severity_level.NORMAL)
def test_update_pet(pet_store, create_base_pet):
    """
    Обновление имеющейся записи с помощью PUT и проверка через GET
    Swagger: /pet Update an existing pet
    """

    with allure.step("1. Создание питомца"):
        created_pet = create_base_pet.json()
        pet_id = created_pet["id"]

        assert create_base_pet.status_code == 200

        allure.attach(
            f"Status created_pet: {create_base_pet.status_code}, \nBody: {created_pet}",
            name="created_pet response",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("2. Обновление питомца"):
        new_name = "updated_json_Murzik"
        pet_data = {"id":pet_id,"name":new_name}
        updated_pet = pet_store.update_pet_json(pet_data)
        assert updated_pet.status_code == 200
        assert updated_pet.json()["id"] == pet_id
        assert updated_pet.json()["name"] == new_name
        assert updated_pet.json()["photoUrls"] == []
        assert updated_pet.json()["tags"] == []

        allure.attach(
            f"Status updated_pet: {updated_pet.status_code}, \nBody: {updated_pet.json()}",
            name="updated_pet response",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("3. Получение питомца из БД"):
        get_pet_from_api = pet_store.get_pet(pet_id)
        actual_pet = get_pet_from_api.json()
        assert get_pet_from_api.status_code == 200

        allure.attach(
            f"Status get_pet: {get_pet_from_api.status_code}, \nBody: {actual_pet}",
            name="get_pet response",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("4. Проверка, что поля обновлены"):
        assert actual_pet["id"] == pet_id
        assert actual_pet["name"] == new_name
        assert actual_pet["photoUrls"] == []
        assert actual_pet["tags"] == []

        allure.attach(
            f"Pet from DB:\n{actual_pet}\n\nCreated pet:\n{created_pet}\nUpdated pet:\n{updated_pet.json()}",
            name="comparison_data",
            attachment_type=allure.attachment_type.TEXT
        )


@pytest.mark.smoke
@allure.title("Получение питомца из API")
@allure.feature("Питомцы")
@allure.severity(allure.severity_level.NORMAL)
def test_get_pet(pet_store, create_base_pet):
    """
    Получение питомца из API
    Swagger: /pet/{pet_id} Find pet by ID
    """

    with allure.step("1. Создание питомца"):
        created_pet = create_base_pet.json()
        pet_id = created_pet["id"]

        assert create_base_pet.status_code == 200

        allure.attach(
            f"Status created_pet: {create_base_pet.status_code}, \nBody: {created_pet}",
            name="created_pet response",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("2. Получение питомца из БД"):
        get_pet_from_api = pet_store.get_pet(pet_id)
        actual_pet = get_pet_from_api.json()
        assert get_pet_from_api.status_code == 200
        assert actual_pet == created_pet

        allure.attach(
            f"Status get_pet: {get_pet_from_api.status_code}, \nBody: {actual_pet}",
            name="get_pet response",
            attachment_type=allure.attachment_type.TEXT
        )


@pytest.mark.smoke
@allure.title("Получение питомца из API. НЕГАТИВНЫЙ ТЕСТ, id  не существует")
@allure.feature("Питомцы")
@allure.severity(allure.severity_level.NORMAL)
def test_get_pet_absent(pet_store):
    """
    Получение питомца из API. НЕГАТИВНЫЙ ТЕСТ, id  не существует
    Swagger: /pet/{pet_id} Find pet by ID
    """

    pet_id = int(time.time())

    with allure.step("1. Получение питомца с несуществуеющим id"):
        response = pet_store.get_pet(pet_id)

        assert response.status_code == 404, (
            f"Ожидался код 404 для несуществующего питомца {pet_id}, "
            f"получен {response.status_code}"
        )

        allure.attach(
            f"Status get_pet: {response.status_code},\nError text: {response.json()} \nPet id: {pet_id}",
            name="get_pet response",
            attachment_type=allure.attachment_type.TEXT
        )
