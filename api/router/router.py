
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Response,FastAPI, File, UploadFile, Depends, Request
from fastapi.responses import JSONResponse
from services.send_email import send_email_with_attachment
from pydantic import BaseModel, Field
import os 
import shutil
from dotenv import load_dotenv
import random
import json
load_dotenv()

router = APIRouter()

from lyzr import QABot
from lyzr import ChatBot

# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

class SendEmail(BaseModel):
    emails: list[str] = Field(..., example=["user1@example.com", "user2@example.com"])

current_directory = os.path.dirname(os.path.abspath(__file__))

reg_form = os.path.join(current_directory, 'registration form.pdf')
upload_folder_reg =  os.path.join(current_directory, 'exports/reg/')
upload_folder_rfp =  os.path.join(current_directory, 'exports/rfp/')
reg_vector_store = os.path.join(current_directory, 'reg_vector_store/.lancedb')
rfp_vector_store = os.path.join(current_directory, 'rfp_vector_store/.lancedb')

Reg_QAbot =None
RFP_QAbot =None

reg_file_path = []
rfp_file_path = []

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
    
########################################################################################################################################################################################################################################
    
@router.post("/goml/LLM marketplace/reg_upload")
async def upload_files(files: list[UploadFile] = File(...)):
    global Reg_QAbot
    global reg_file_path
    try:
        # Create the upload folder if it doesn't exist
        
        if not os.path.exists(reg_vector_store):
            # shutil.rmtree(os.path.join(current_directory, 'reg_vectore_store'))
            os.makedirs(reg_vector_store)
        if os.path.exists(upload_folder_reg):
            shutil.rmtree(upload_folder_reg)
        reg_file_path.clear()
        if not os.path.exists(upload_folder_reg):
            os.makedirs(upload_folder_reg)
        print(upload_folder_reg)
        for file in files:
            file_path = os.path.join(upload_folder_reg, file.filename)
            reg_file_path.append(file_path)
            # Save the file to the specified folder
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)


        random_integer = random.randint(1, 10000000000)
        table_name = "reg"+str(random_integer)
        Reg_QAbot = ChatBot.pdf_chat(input_files=reg_file_path,
        vector_store_params={
            "vector_store_type": "LanceDBVectorStore",
            "uri":reg_vector_store,
            "table_name": table_name,
        }
    )
  
        
        return JSONResponse(content={"message": "Files uploaded successfully"}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/goml/LLM marketplace/Reg_QAbot")
async def upload_files(querys:str):
    global Reg_QAbot
    try:
        response = Reg_QAbot.chat(querys)

        # Print the QABot's response
        print(response.response)
        result = response.response
        return {"response":result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/goml/LLM marketplace/Reg_Matrix")
async def Reg_matrix_generation():
    global reg_file_path
    global Reg_QAbot
    try:
        result_list=[]
        prompt = """you are given with the data of registration forms, fetch the below listed data as matrix and return that as dict, nothing other than that
details:
                                   
Registered Name 

Registered Address 

Contact email id 

Contact Name 

Contact Phone No 

Vendor website 
        
output formate:
list of dict : [{},{}]
        """
        

        response = Reg_QAbot.chat(prompt)

        # Print the QABot's response
        result = eval(response.response)
        json_string = json.dumps(result)

        python_dict = json.loads(json_string)

        # Print the QABot's response
        
        return {"response": python_dict}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#######################################################################################################################################################################################

@router.post("/goml/LLM marketplace/rfp_upload")
async def upload_files(files: list[UploadFile] = File(...)):
    global RFP_QAbot
    global rfp_file_path
    try:
        # Create the upload folder if it doesn't exist
        rfp_file_path.clear()
        if not os.path.exists(rfp_vector_store):
            print("k")
            # os.remove(os.path.join(current_directory, 'reg_vectore_store'))
            os.makedirs(rfp_vector_store)
        if os.path.exists(upload_folder_rfp):
            shutil.rmtree(upload_folder_rfp)

        if not os.path.exists(upload_folder_rfp):
            os.makedirs(upload_folder_rfp)
        print(upload_folder_rfp)
        for file in files:
            file_path = os.path.join(upload_folder_rfp, file.filename)
            rfp_file_path.append(file_path)
            # Save the file to the specified folder
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

        random_integer = random.randint(1, 10000000000)
        table_name = "Rfp"+str(random_integer)
        
        RFP_QAbot = QABot.pdf_qa(input_files=rfp_file_path,
                                 llm_params={"model": "gpt-3.5-turbo"},
        vector_store_params={
            "vector_store_type": "LanceDBVectorStore",
            "uri":rfp_vector_store,
            "table_name": table_name,
        }
    )
        
        print(RFP_QAbot)
        return JSONResponse(content={"message": "Files uploaded successfully"}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/goml/LLM marketplace/RFP_QAbot")
async def upload_files(querys:str):
    global RFP_QAbot
    print(RFP_QAbot)
    try:
        response = RFP_QAbot.query(querys)

        # Print the QABot's response
        print(response.response)
        result = response.response
        return {"response":result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/goml/LLM marketplace/RFP_Matrix")
async def RFP_matrix_generation():
    global RFP_QAbot
    try:
        prompt = """you are given with the data of multiple RFP forms from same or different vendors, extract the below listed data as matrix for all the pdfs,if no exact data found use relavent data and return that as dict, nothing other than that
details:
                                   
1. Vendor Name 

2. Project Title 

3. Delivery Timelines 

4. Commercial quote 

5. References 

6. Payment Timeline 


   7. Year of incorporation 

   8. Total revenue for last year 

   9 Certifications – ISO/GDPR compliant 
        
output format:
list of dict : [{},{}]
        """
        response = RFP_QAbot.query(prompt)

        result = eval(response.response)
        json_string = json.dumps(result)

        python_dict = json.loads(json_string)
        

        return JSONResponse(content={"response":python_dict}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/goml/LLM marketplace/RFP_report")
async def RFP_matrix_generation():
    global rfp_file_path
    try:
        result_list=[]
        prompt = """you are given with the data of multiple RFP forms from same or different vendors, extract the below listed data as matrix for all the pdfs,if no exact data found use relavent data and return that as dict, nothing other than that
                                   
The engine should be able to extract the following details from the document & tabulate for comparison across the 3 contracts.
details:

1)	Vendor Name
2)	Scope of work – Summary in 1 line
3)	Architecture description – Highlight the best practices in 2-3 lines
4)	Project timeline
5)	Commercials, to be shown as a split in the following format
    a.	Implementation costs
    b.	Infrastructure costs
        i.	With Mongo
        ii.	With DocumentDB
6)	Payment milestones
7)	Payment release date
8)	From the internet, it should populate
    a.	Vendor’s date of inception, when did they start operations
    b.	2023 revenue
    c.	Total no of employees
    d.	Any awards/recognitions

        
output format:
dict : {}
        """
        for i in rfp_file_path:
            random_integer = random.randint(1, 100000000000000)
            table_name = "Rfp_report"+str(random_integer)
            
            RFP_reportQAbot = QABot.pdf_qa(input_files=[i],
                                    llm_params={"model": "gpt-3.5-turbo"},
            vector_store_params={
                "vector_store_type": "LanceDBVectorStore",
                "uri":rfp_vector_store,
                "table_name": table_name,
            }
        )
            response = RFP_reportQAbot.query(prompt)

            # Print the QABot's response
            print(response.response)
            result = eval(response.response)
            json_string = json.dumps(result)

            python_dict = json.loads(json_string)
            print(type(response),type(json_string),type(python_dict))
            result_list.append(python_dict)
        return {"response":result_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
