import boto3
import json
import os
from dotenv import load_dotenv, find_dotenv
import re

load_dotenv(find_dotenv())

# AWS_ACCESS_KEY_ID=os.environ.get("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY_ID=os.environ.get("AWS_SECRET_ACCESS_KEY_ID")
# region_name = os.environ.get("region_name")

# bedrock = boto3.client(aws_access_key_id=AWS_ACCESS_KEY_ID, 
#                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY_ID,
#                       service_name='bedrock',region_name=region_name,
#                       endpoint_url='https://bedrock.us-west-2.amazonaws.com')
region_name = os.environ.get("region_name")

os.environ['AWS_ACCESS_KEY_ID'] = "AKIA3OBOBB2KA5Y7LLIT"

os.environ['AWS_SECRET_ACCESS_KEY'] = "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"

 

bedrock = boto3.client(aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],

                      aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],

                      service_name='bedrock',region_name=region_name,

                      endpoint_url='https://bedrock.us-west-2.amazonaws.com')

def aws_claude_summarisation(payload):
    text=payload['text']
    # summary="write summary:"
    
    # print(text)
    summary="provide me only the company name, cost ,  website and time line from the text that is provided. if company name, cost , website and time line is not present return me with 'N/A' dont provide me anything else"
    body_json = {
    "prompt": f"Human: {summary} {text} give me output in the form of a list of JSON. "
              f"The structure of the output should look like this only, for example: "
              f"[{{'company_name': 'ABC Corporation', 'cost': '324', 'website': 'https://www.abccorp.com', 'timeline': '3months'}}, "
              f"{{'company_name': 'XYZ Builders Inc.', 'cost': '34', 'website': 'https://www.abccorp.com', 'timeline': '2months'}}] "
              f"this is just an example for two companies. Give me output in the exact structure for all the companies mentioned in the text provided. "
              f"One dictionary for one company and add it to the list. Don't give me anything apart from a list of dictionaries Assistant:",
    "max_tokens_to_sample": 300,
    "temperature": 1,
    "top_k": 250,
    "top_p": 0.999,
    "stop_sequences": ["Human:"],
    "anthropic_version": "bedrock-2023-05-31"
    }

    body = json.dumps(body_json)
    print(body)
    modelId = 'anthropic.claude-v2'
    accept = 'application/json'
    contentType = 'application/json'

    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    print(response_body)


    result=response_body.get('completion')
    
    return {'output':result}


# dict1 = { "text" : """Provide me only the cost , website and time in days for all the company names in the given list seperatedly , {'ABC Corporation': [{'RFP no': '12345', 'RFP date': '2023-08-15', 'Request proposal document for ': 'IT Services', 'company name': 'ABC Corporation', 'phone number': '+1 (555) 123-4567', 'email id': 'info@abccorp.com', 'website': 'https://www.abccorp.com', 'last date for submission': '2023-09-30', 'date of opening': '2023-10-10', 'time of opening': '10:00 AM', 'signature date': '2023-08-20', 'chief officer signature': 'John Doe', 'address': '123 Main Street, Anytown, USA', 'introduction': 'This request for proposal (RFP) is issued to invite proposals for IT services.', 'scope of the work': 'The scope includes software development, system integration, and maintenance.', 'guideline for the biders': 'Bidders must follow the guidelines provided in the RFP document.', 'Technical requirements ': 'The solution must be compatible with Windows and Linux environments.', 'Data preprocessing or Research and development': 'Data preprocessing is a critical part of the project.', 'model development': 'Machine learning models will be developed for predictive analytics.', 'integration': 'Integration with existing systems is required.', 'user interface and experience ': 'A user-friendly interface is essential for this project.', 'Evaluation metrics': 'Performance will be evaluated based on accuracy, speed, and reliability.', 'timeline': 'The project is expected to be completed within 12 months.', 'security and privacy': 'Data security and privacy are top priorities for this project.', 'deployment and maintenance': 'Ongoing maintenance and support will be needed after deployment.', 'scalability and performance': 'The solution must be scalable to handle increased workloads.', 'additional notes': 'Any additional information or requirements can be found in the RFP document.', 'budget requirements': '$1,000,000'}, {'to address': 'Neural go', 'Quote date': '21/08/2023', 'Quote number': '1', 'customer id': '123', 'valid until': '09/09/2023', 'company name': 'ABC Corporation', 'name': 'Akash', 'address': 'Coimbatore', 'email': 'csakash03@gmail.com', 'phone': '12345', 'sign date': '21/08/2023', 'signature ': 'Akash', 'item 1': '1', 'sub total': '1080', 'tax': '10%', 'tax rate': '108', 'shipping price': '100', 'total 1': '1080', 'discount 1': '10', 'unit price 1': '1200', 'quantity  1': '1', 'description 1': 'computer' , 'time' : '5 Days'}], 
# 'XYZ Builders Inc.': [{'RFP no': 'RFQ2023-6789', 'RFP date': '2023-09-15', 'Request proposal document for ': 'Construction Services', 'company name': 'XYZ Builders Inc.', 'phone number': '+1 (555) 789-1234', 'email id': 'info@xyzbuilders.com', 'website': 'https://www.xyzbuilders.com', 'last date for submission': '2023-10-31', 'date of opening': '2023-11-15', 'time of opening': '2:00 PM', 'signature date': '2023-09-20', 'chief officer signature': 'Jane Smith', 'address': '456 Oak Street, Constructionville, USA', 'introduction': 'This RFP solicits proposals for a construction project for a new office building.', 'scope of the work': 'Scope includes architectural design, construction, and interior finishing.', 'guideline for the biders': 'Bidders must adhere to safety and quality standards outlined in the RFP.', 'Technical requirements ': 'Construction materials must meet local building codes and standards.', 'Data preprocessing or Research and development': 'Not applicable to this construction project.', 'model development': 'Architectural and structural models will be developed prior to construction.', 'integration': 'Integration of various construction phases is crucial for project success.', 'user interface and experience ': 'Focus is on functionality and safety, not a user interface.', 'Evaluation metrics': 'Performance will be evaluated based on project milestones and quality standards.', 'timeline': 'Construction is expected to be completed within 18 months.', 'security and privacy': 'Security measures will be in place to protect the construction site.', 'deployment and maintenance': 'Maintenance after construction completion will be minimal.', 'scalability and performance': 'Not applicable to construction services.', 'additional notes': 'Interested bidders should attend a pre-proposal meeting on 2023-10-05.', 'budget requirements': '$5,000,000'}, {'to address': 'Neural go', 'Quote date': '21/08/2023', 'Quote number': '1', 'customer id': '123', 'valid until': '09/09/2023', 'company name': 'XYZ Builders Inc.', 'name': 'Akash', 'address': 'Coimbatore', 'email': 'csakash03@gmail.com', 'phone': '12345', 'sign date': '21/08/2023', 'signature ': 'Akash', 'item 1': '1', 'sub total': '1080', 'tax': '10%', 'tax rate': '108', 'shipping price': '100', 'total 1': '108', 'discount 1': '10', 'unit price 1': '1200', 'quantity  1': '1', 'description 1': 'computer' , 'time' : '3 Days'}],
# 'goml': [{'RFP no': 'RFQ2023-6783', 'RFP date': '2023-09-15', 'Request proposal document for ': 'AI products', 'company name': 'goml', 'phone number': '+1 (555) 789-1234', 'email id': 'info@xyzbuilders.com', 'website': 'https://www.xyzbuilders.com', 'last date for submission': '2023-10-31', 'date of opening': '2023-11-15', 'time of opening': '2:00 PM', 'signature date': '2023-09-20', 'chief officer signature': 'Jane Smith', 'address': '456 Oak Street, Constructionville, USA', 'introduction': 'This RFP solicits proposals for a construction project for a new office building.', 'scope of the work': 'Scope includes architectural design, construction, and interior finishing.', 'guideline for the biders': 'Bidders must adhere to safety and quality standards outlined in the RFP.', 'Technical requirements ': 'Construction materials must meet local building codes and standards.', 'Data preprocessing or Research and development': 'Not applicable to this construction project.', 'model development': 'Architectural and structural models will be developed prior to construction.', 'integration': 'Integration of various construction phases is crucial for project success.', 'user interface and experience ': 'Focus is on functionality and safety, not a user interface.', 'Evaluation metrics': 'Performance will be evaluated based on project milestones and quality standards.', 'timeline': 'Construction is expected to be completed within 18 months.', 'security and privacy': 'Security measures will be in place to protect the construction site.', 'deployment and maintenance': 'Maintenance after construction completion will be minimal.', 'scalability and performance': 'Not applicable to construction services.', 'additional notes': 'Interested bidders should attend a pre-proposal meeting on 2023-10-05.', 'budget requirements': '$5,000,000'}, {'to address': 'goml', 'Quote date': '21/08/2023', 'Quote number': '1', 'customer id': '123', 'valid until': '09/09/2023', 'company name': 'goml', 'name': 'Akash', 'address': 'Coimbatore', 'email': 'csakash03@gmail.com', 'phone': '12345', 'sign date': '21/08/2023', 'signature ': 'Akash', 'item 1': '1', 'sub total': '1080', 'tax': '10%', 'tax rate': '108', 'shipping price': '100', 'total': '980', 'discount 1': '10', 'unit price 1': '1200', 'quantity  1': '1', 'description 1': 'computer', 'time' : '3 Days'}]
# }"""
# }

# result = aws_claude_summarisation(dict1)
# print(result)


def extract_list_from_text(input_text):
    json_string = input_text.replace("'", '"')

    try:
        start_index = json_string.find("[")
        end_index = json_string.rfind("]") + 1

        if start_index != -1 and end_index != -1:
            json_content = json_string[start_index:end_index]

            data_list = json.loads(json_content)
            if isinstance(data_list, list):
                return data_list
            else:
                return None
        else:
            return None
    except json.JSONDecodeError:
        return None


# result = extract_list_from_text(text1)