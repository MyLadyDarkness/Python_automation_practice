from src.api.client import Client


class PetStore(Client):

#------------------------All about pet--------------------
    def create_pet(self, pet_data):
        return self.post("/pet", data=pet_data)

    def get_pet(self, pet_id):
        return self.get(f"/pet/{pet_id}")
