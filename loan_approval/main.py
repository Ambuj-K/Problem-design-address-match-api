from fastapi import FastAPI
from pydantic import BaseModel

from .api_functions.reject_status import *
from .api_functions.supporter import *

app = FastAPI()


# declaring message model for incoming api requests
class UserDetails(BaseModel):
    customerID: int
    dob: str
    income: float
    bureauScore: int
    applicationScore: int
    maxDelL12M: int
    allowedFoir: int
    existingEMI: int
    loanTenure: int
    currentAddress: str
    bureauAddress: str


# loan approval functions
@app.post("/loan_approval/")
async def loan_approval(input_data: UserDetails):

    # calculate age
    age = age_string_calculator(input_data.dob)
    # address match percentage
    address_matching_score = matching(input_data.currentAddress,
                                      input_data.bureauAddress)
    # check each condition set reject log and flag status
    reject_status_array = calculate_loan_prerequisites(age, input_data.income,
                                                       input_data.bureauScore,
                                                       input_data.applicationScore,
                                                       input_data.maxDelL12M,
                                                       address_matching_score)

    reject_flag = reject_status_array[0]
    reject_log = reject_status_array[1]

    loanamount = calculate_line_assign(input_data.allowedFoir,
                                       input_data.income,
                                       input_data.existingEMI,
                                       input_data.loanTenure)
    # calculate loan amount and set reject flag and log
    loantenure = input_data.loanTenure

    # assign approval status after all computations for response payload
    approvalstatus = "Rejected" if reject_flag else "Approved"

    # generic elements regardless of approve/reject call
    response = {"approvalStatus": approvalstatus,
                "addressMatchingScore": address_matching_score}

    # add extra elements based on approve/reject
    if approvalstatus == "Approved":
        response["loanAmount"] = loanamount
        response["loanTenure"] = loantenure
        return response
    else:
        reject_code = reject_log
        response["reject_code"] = reject_code
        return response
