import pytest

from src.api.endpoints.petstore import PetStore
from src.utils.unique_id_gen import generated_unique_id

@pytest.fixture(scope="session", autouse=True)
def pet_store():
    return PetStore("https://petstore.swagger.io/v2")

@pytest.fixture(scope="function")
def base_pet_data():
    pet_data = {
        "id":f"{generated_unique_id()}",
        "name": f"test_pet_{generated_unique_id()}",
        "photoUrls": ["string"]
    }
    return pet_data

@pytest.fixture(scope="function")
def full_pet_data(base_pet_data):
    state = "available"
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
        "status": state
    }

@pytest.fixture(scope="function")
def create_base_pet(pet_store, base_pet_data):
    response = pet_store.create_pet(base_pet_data)
    #pet = response.json()

    yield response

    pet_store.delete_pet(response.json()["id"])

