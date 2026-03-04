import pytest

from src.api.endpoints.petstore import PetStore
from src.utils.unique_id_gen import generated_unique_id

@pytest.fixture(scope="session", autouse=True)
def pet_store():
    return PetStore("https://petstore.swagger.io/v2")

@pytest.fixture(scope="function")
def base_pet_data():
    unique_number = generated_unique_id()
    pet_data = {
        "id":f"{unique_number}",
        "name": f"test_pet_{unique_number}",
        "photoUrls": ["string"]
    }
    return pet_data

@pytest.fixture
def status():
    return "available"

@pytest.fixture(scope="function")
def all_pet_data_no_state(base_pet_data, status):
    pet_data = {
        **base_pet_data,
        "category": {
            "id": base_pet_data["id"],
            "name": f"test_pet_{base_pet_data['id']}"
        },
        "tags": [
            {
                "id": base_pet_data["id"],
                "name": f"test_pet_{base_pet_data['id']}"
            }
        ],
        "status": status
    }
    return pet_data

@pytest.fixture(scope="function")
def create_base_pet(pet_store, base_pet_data):
    response = pet_store.create_pet(base_pet_data)

    yield response

    pet_store.delete_pet(response.json()["id"])

@pytest.fixture(scope="function")
def create_full_pet(pet_store, all_pet_data_no_state):
    response = pet_store.create_pet(all_pet_data_no_state)

    yield response

    pet_store.delete_pet(response.json()["id"])