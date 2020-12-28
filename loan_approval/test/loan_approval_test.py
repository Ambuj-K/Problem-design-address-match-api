from fastapi.testclient import TestClient
from loan_approval.main import *

client = TestClient(app)


def test_loan_approval():
    # response = client.get("/")

    resp = client.post("/loan_approval/", json={
        "customerID": 100000,
        "dob": "01/01/1970",
        "income": 2500,
        "bureauScore": 400,
        "applicationScore": 750,
        "maxDelL12M": 0,
        "allowedFoir": 60,
        "existingEMI": 2000,
        "loanTenure": 24,
        "currentAddress": "15 2nd cross vagd 560037 layout Marathahalli Bangalore "
                          "Karnataka",
        "bureauAddress": "15 2nd cross vagdevi layo Marathahalli Bangalore "
                          "Karnataka 560037"
    })

    # need to add assert to make it part of code check
    print(resp.json())
    # assert (resp.json() == {'approvalStatus': 'Rejected',
    #                         'addressMatchingScore':
    #                             74,
    #                         'reject_code': '506 AddressMatchingScore LT 80'})


test_loan_approval()
