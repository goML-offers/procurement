import sys
import time
from fastapi import FastAPI, File, Form, UploadFile
sys.path.insert(0, 'LLM Procurement\\api\\')
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Response
from schemas.schemas import FileUpload,EmailFile,SendEmail,FilePath,Prompt,Send_Email
from services.registration_validation import registration_validation
from services.RFP_validation import rfp_validation,rfp_data_extraction
from services.merge_data import merge_by_company_name
# from services.local_data import get_from_local,push_to_local
from services.send_email import send_email_with_attachment
from services.crawler import crawler, output , extract, suggestion
from services.bedrock_claude import aws_claude_summarisation, extract_list_from_text
from services.s3_data import push_to_s3,get_from_s3
import os
from fastapi.responses import JSONResponse
import shutil
import json
from dotenv import load_dotenv
load_dotenv()

reg_form=os.environ.get("reg_form")
rfp_form = os.environ.get("rfp_form")
txt_data=os.environ.get("txt_data")
# Email configuration

router = APIRouter()

@router.post('/goml/LLM marketplace/vendor_suggestion', status_code=201)
def matrix_generator_from_RFP(data:Prompt):
    vendor_suggestion = suggestion(data.prompt)
    return vendor_suggestion["output"]

@router.post("/goml/LLM marketplace/send_custom_form")
async def upload_file(data: Send_Email):
    try:
        file_paths=[]
        for file_path in data.file:
                # Save the uploaded file to the 'uploads' directory
                print(file_path)
                
                with open(file_path, "rb") as f:
                    file = UploadFile(file=f, filename=os.path.basename(file_path))
                    
                    with open(file.filename, "wb") as dest_f:
                        shutil.copyfileobj(file.file, dest_f)
                    file_paths.append(file.filename)
        
        send_email_with_attachment(data.subject,data.body,data.email,file_paths)
        return "Mail sent with form successfully"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post('/goml/LLM marketplace/send_registration_form', status_code=201)
def send_registration_form(data: SendEmail):
    try:
        subject = "Request for Vendor Registration Form"
        body = """
        Dear Vendor,

        I hope this email finds you well. We are interested in establishing a vendor relationship with your company and would like to request a vendor registration form to initiate the process. Your products/services align with our requirements, and we believe that a partnership with your organization would be mutually beneficial.

        To ensure a smooth onboarding process, we kindly request that you provide us with the necessary vendor registration form or documentation. This will allow us to gather essential information about your company, products, pricing, and terms of service.

        If you have a specific vendor registration process or form unique to your organization, kindly share it with us at your earliest convenience. We understand that each company may have its own set of requirements, and we are committed to meeting them.

        Once we have completed the registration process, we look forward to exploring potential collaboration opportunities and establishing a long-lasting business relationship.

        If you have any questions or need further information, please do not hesitate to contact us.

        Thank you for your prompt attention to this request. We appreciate your time and consideration.

        Sincerely,
        Your Company Name"""
        for email in data.emails:
            send_email_with_attachment(subject,body,email,reg_form)
        return "Email sent successfully"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/goml/LLM marketplace/send_RFP_form', status_code=201)
def send_RFP_form(data: SendEmail):
    print("satish")
    try:
        
        subject = "Request for Proposal (RFP) Submission"
        body = """
        Dear Recipient,

        I hope this email finds you well. We are currently seeking proposals for a project and would like to invite your organization to submit a proposal.

        To facilitate the submission process, we kindly request that you complete the attached RFP form. If your organization has specific RFP submission guidelines or requirements, please provide those documents along with your proposal.

        [Attach RFP Form - If Applicable]

        Please submit your completed proposal and any additional documentation to [Submission Email Address] by [Submission Deadline]. If you have any questions or require further information, please do not hesitate to contact us.

        We look forward to receiving your proposal and potentially collaborating with your organization.

        Thank you for considering our request.

        Sincerely,
        Your Company Name"""
        try: 
            for email in data.emails:
                send_email_with_attachment(subject,body,email,rfp_form)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail=str(e))
        return "Email sent successfully"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.post('/goml/LLM marketplace/vendor_registration', status_code=201)
def registration_form_validation_and_data_extraction(data: FileUpload):
    try:
        os.makedirs("/app/registration_uploads", exist_ok=True)
        
        validation_results = []
        print(data.files)
        for email, file_path in zip(data.emails, data.files):
            # Save the uploaded file to the 'uploads' directory
            with open(file_path, "rb") as f:
                file = UploadFile(file=f, filename=os.path.basename(file_path))
                file_path_dest = os.path.join("/app/registration_uploads", file.filename)
                with open(file_path_dest, "wb") as dest_f:
                    shutil.copyfileobj(file.file, dest_f)
            push_to_s3(file_path_dest,data.company_name)
            # Call your registration validation function
            validation_result = registration_validation(file_path, email)
            if validation_result is None:
                continue
            validation_results.append(validation_result)

        # os.remove(file_path_dest)
        # if not validation_result:
        #     return "None of the given form is valid"
        # obj = registration_validation(file_path,email)
        print(validation_results)
        # push_to_local(validation_results,data.company_name)
        
        # os.remove(file_path)
        
        return "Successfully analyzed and sent email"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post('/goml/LLM marketplace/RFP_registration', status_code=201)
def RPF_form_validation_and_data_extraction(data: FileUpload):
    try:
        os.makedirs("/app/RFP_uploads", exist_ok=True)

        validation_results = []
        path = []
        for email, file_path in zip(data.emails, data.files):
            # Save the uploaded file to the 'uploads' directory
            print(file_path)
            
            with open(file_path, "rb") as f:
                file = UploadFile(file=f, filename=os.path.basename(file_path))
                file_path_dest = os.path.join("/app/RFP_uploads", file.filename)
                with open(file_path_dest, "wb") as dest_f:
                    shutil.copyfileobj(file.file, dest_f) 
            print("fp",file_path)
            #path.append(file_path_dest)
            path.append(push_to_s3(file_path_dest,data.company_name))
            # Call your registration validation function
            validation_result = rfp_validation(file_path, email)
            # os.remove(file_path_dest)
            if validation_result is None:
                continue
            
            # os.remove(file_path)

        # if not validation_results:
        #     return "None of the given form is valid"
        # rfp_data = get_from_local(data.company_name)
        # print(type(rfp_data),type(rfp_data[0]))
        
        # merged_data =  merge_by_company_name(rfp_data,validation_results)
        # obj = registration_validation(file_path,email)
        # print(merged_data)
        # os.remove(file_path)


        # return "Successfully analyzed and sent email"
        # return validation_results
        print(path)
        return path
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/goml/LLM marketplace/Matrix_generator', status_code=201)
def matrix_generator_from_RFP(data: FilePath):
    try:
        x=((data.file_path[0]).split("\\"))
        txt_name = x[-1].split('.')[0]
        print(data.file_path,"file_path",x)
        # txt_name  = "akaash"
        validation_results = []
        for files in data.file_path:
            
            files = get_from_s3(files)
            print(files)
            validation_results.append(rfp_data_extraction(files))
        
        print(validation_results)
        data = {'text': f"Provide me only the total cost and time for all the compnay names in the given list seperatedly {validation_results}"}
        llm_data = aws_claude_summarisation(data)
        print(llm_data['output'])
        print("---------------------------------------formatting data------------------------------------------")
        llm_formatted_data = extract_list_from_text(llm_data['output'])
        print(llm_formatted_data)
        print("---------------------------------------crawler data------------------------------------------")
        crawler_formatted_data = crawler(llm_formatted_data)
        print(crawler_formatted_data)
        extracted_data  = extract(crawler_formatted_data)
        print(extracted_data)
        matrix = output(extracted_data, llm_formatted_data)
        print("matrix ----------------------------",matrix)
        # return matrix
        my_dictionary=[]
        if len(matrix)!=0:
            my_dictionary = matrix
        # folder_path = txt_data

        # try:
        #     # Create the folder if it doesn't exist
        #     os.makedirs(folder_path, exist_ok=True)

        #     # Define the file path
        #     file_path = os.path.join(folder_path, txt_name+'.txt')

        #     # Open the file in write mode
        #     with open(file_path, 'w') as file:
        #         # Write the dictionary as a string representation to the file
        #         file.write(str(my_dictionary))

        #     print(f"Dictionary stored in {file_path}")
        # except Exception as e:
        #     print(f"Error: {str(e)}")
        # # print(data.file_name)
        return matrix
    except Exception as e:
        print(f"Error: {str(e)}")
        return e

@router.post('/goml/LLM marketplace/uploadFile', status_code=201)
def send_registration_form(file: UploadFile):
    UPLOAD_DIR = "/app/uploads"

    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    # Generate a unique file name to avoid overwriting existing files
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as f:
        f.write(file.file.read())
        f.close()
    

    return {"file_path": file_path}

import os
import ast

# @router.get('/goml/LLM marketplace/Matrix_generator_data', status_code=201)
# def extract_and_remove_dicts_from_files():
#     folder_path = txt_data
#     try:
#         # Get a list of all .txt files in the folder
#         txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

#         # Initialize an empty list to store the extracted dictionaries
#         extracted_dicts = []

#         # Loop through each .txt file
#         for txt_file in txt_files:
#             file_path = os.path.join(folder_path, txt_file)

#             # Read the file contents
#             with open(file_path, 'r') as file:
#                 file_contents = file.read()

#             try:
#                 # Convert the file contents to a dictionary using ast.literal_eval
#                 extracted_dict = ast.literal_eval(file_contents)

#                 # Append the extracted dictionary to the list
#                 extracted_dicts.append(extracted_dict)

#                 print(f"Extracted dictionary from {txt_file}")
#             except (SyntaxError, ValueError):
#                 print(f"Skipped {txt_file} - Not a valid dictionary")

#         return extracted_dicts
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return []

from fastapi import FastAPI, HTTPException, Form
import boto3
 

 

