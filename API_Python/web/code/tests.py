import app
from fastapi.testclient import TestClient

client = TestClient(app.app)
baseUrl = app.baseUrl


def testGetEmployee():
    response = client.get(baseUrl)
    assert response.status_code == 200


def testCreateEmployee():
    response = client.post(
        baseUrl, json={"firstName": "pierre2", "lastName": "bouscailloux4", "emailId": "email"})
    try:
        assert response.status_code == 201
    except:
        print(response)
        raise Exception(response)


def testGetEmployeebyID():
    idEmployee = client.get(baseUrl).json()[-1]["id"]
    response = client.get(baseUrl+"/"+str(idEmployee))
    assert response.status_code == 200


def testUpdateEmployee():
    try:
        idEmployee = client.get(baseUrl).json()[-1]["id"]
        response = client.put(baseUrl+"/" + str(idEmployee), json={
                              "firstName": "pierre2",    "lastName": "bouscailloux12",    "emailId": "email"})
        assert response.status_code == 200
    except:
        raise Exception(idEmployee, response)


def testDeleteEmployee():
    try:
        idEmployee = client.get(baseUrl).json()[-1]["id"]
        response = client.delete(baseUrl + "/" + str(idEmployee))
        assert response.status_code == 200
    except:
        raise Exception(idEmployee, response)


if __name__ == "__main__":
    testGetEmployee()
    print("get ALL ok ")
    testGetEmployeebyID()
    print("test by id ok")
    testCreateEmployee()
    print("test create ok")
    testUpdateEmployee()
    print("test update ok ")
    testDeleteEmployee()
    print("test delete ok ")
    print("ok")
