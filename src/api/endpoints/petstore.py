from src.api.client import Client


class PetStore(Client):

#------------------------All about pet--------------------
    def create_pet(self, pet_data):
        return self.post("/pet", json = pet_data)

    def update_pet_form_data(self, pet_id, name=None, status=None):
        pet_data = {}

        if name:
            pet_data["name"] = name
        if status:
            pet_data["status"] = status

        return self.post(f"/pet/{pet_id}", data = pet_data)


    def get_pet(self, pet_id):
        return self.get(f"/pet/{pet_id}")

    def get_pet_by_status(self, pet_status):
        return self.get(f"/pet/findByStatus", params={"status": pet_status})

    def edit_pet(self, pet_data):
        return self.put("/pet", json=pet_data)

    def delete_pet(self, pet_id):
        return self.delete(f"/pet/{pet_id}")