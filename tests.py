import requests
import random
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

def test_fetch_persons():
    response = requests.get(f"{BASE_URL}/api")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    print("Fetch persons case passed!")

def test_create_person(return_person=False):
    person_data = {
        "email": f"test{random.randrange(400, 5000)}@example.com",
        "first_name": "John",
        "last_name": "Doe",
    }
    response = requests.post(f"{BASE_URL}/api", json=person_data)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["email"] == person_data["email"]
    assert data["first_name"] == person_data["first_name"]
    assert data["last_name"] == person_data["last_name"]

    print("Create person case passed!")

    if return_person:
        return data

def test_fetch_person():
    person = test_create_person(return_person=True)
    
    person_id = person["id"]
    response = requests.get(f"{BASE_URL}/api/{person_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["id"] == person_id

    test_delete_person(person["id"])

    print("Fetch person case passed!")


def test_update_person():
    person = test_create_person(return_person=True)
    
    updated_data = {
        "email": "updated@example.com",
        "first_name": "UpdatedFirstName",
        "last_name": "UpdatedLastName",
    }
    response = requests.patch(f"{BASE_URL}/api/{person['id']}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["email"] == updated_data["email"]
    assert data["first_name"] == updated_data["first_name"]
    assert data["last_name"] == updated_data["last_name"]

    print(person["id"])

    test_delete_person(person["id"])

    print("Update person test case passed!")

def test_delete_person(provided_id=None):
    person = test_create_person(return_person=True)
    person_id = person["id"] if not(provided_id) else provided_id

    response = requests.delete(f"{BASE_URL}/api/{person_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data == {"status": "success", "message": "successfully delete person"}



if __name__ == "__main__":
    # Run the tests
    test_fetch_persons()
    test_create_person()
    test_fetch_person()
    test_update_person()
    test_fetch_persons()
    test_delete_person()

    print("All test cases passed!")
