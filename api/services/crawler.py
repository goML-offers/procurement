import boto3
import json
import os
from dotenv import load_dotenv, find_dotenv
import re
import requests
from bs4 import BeautifulSoup
import ast

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
    summary="find me only the company name and the certification name or any award mentioned and the annual revenue from the text that is provided. if name of the company or certification name or the annual revenue is not present return me with 'N/A' dont provide me anything else"
    body_json = {
    "prompt": f"Human: {text} {summary} give me output in the form of a JSON like structure. "
              f"The structure of the output should look like this only, for example: "
              f"{{'company_name': 'ABC Corporation', 'certification': 'ISO certified', 'annual_revenue': '$23243434'}} and one more example"
              f"{{'company_name': 'XYZ Builders Inc.', 'certification': 'ISO certified name', 'annual_revenue': '$2300434'}}"
              f"this is just an example for one company. Give me output in the exact structure and format nothing else should be given extra for the company mentioned in the text provided. "
              f"One dictionary for the company only, so the list should have only those number of dictionaries that are mentioned in the give text. Don't give me anything apart from dictionary if anything is not present or mentionted give 'N/A' for that key only Assistant:",
    "max_tokens_to_sample": 300,
    "temperature": 1,
    "top_k": 250,
    "top_p": 0.999,
    "stop_sequences": ["Human:"],
    "anthropic_version": "bedrock-2023-05-31"
    }

    body = json.dumps(body_json)
    
    # print(body)
    modelId = 'anthropic.claude-v2'
    accept = 'application/json'
    contentType = 'application/json'

    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())

    result=response_body.get('completion')
    
    return {'output':result}

# result = aws_titan_summarisation(dict_pagecontent)

# # list_dict = [{'company_name': 'scnsoft', 'cost': '200', 'website': 'https://www.aalpha.net/', 'time': 'N/A'}]
# list_dict = [{'vendor_name': 'Saigon Technology', 'cost': '227,250', 'website': 'https://saigontechnology.com/', 'time': 'N/A'}, {'vendor_name': 'Aalpha Information Systems', 'cost': '227,250', 'website': 'https://www.aalpha.net/', 'time': 'N/A'}]
def crawler(list_dict):

    dict_col = []

    for li in list_dict:
        print(li['website'])
        response = requests.get(li['website'])
        print(response.status_code)
        print("----------------------------------------------------------------------------------------")
        # print(page_content)
        # print(type(page_content))
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup.get_text())
        dict_pagecontent = {'text': soup.get_text()}
        result = aws_claude_summarisation(dict_pagecontent)
        dict_col.append(result['output'])
        print(type(result['output']))
    return dict_col

# crawler_result = crawler(list_dict)


def extract(crawler_result):
    # print("crawler_result--------------------------",crawler_result)
    parsed_data = []
    pattern = r'\{[^}]*\}'

    for data in crawler_result:
        matches = re.findall(pattern, data)
        for match in matches:
            try:
                dictionary = json.loads(match)
                if isinstance(dictionary, dict):
                    parsed_data.append(dictionary)
            except ValueError:
                pass
    print(parsed_data)
    return parsed_data

# extract_data_crawl = extract(crawler_result)



def output(crawler_data,llm_data):
    
    new_list = []
    for crawl_list in crawler_data:
        for llm_list in llm_data:
            if crawl_list['company_name'] in llm_list['company_name']:
                new_dict = {}
                new_dict['company_name'] = llm_list['company_name']
                new_dict['cost'] = llm_list['cost']
                new_dict['timeline'] = llm_list['valid_until']
                new_dict['certification'] = crawl_list['certification']
                new_dict['annual_revenue'] = crawl_list['annual_revenue']
                new_list.append(new_dict)
            else:
                pass
    print(new_list)
    return new_list
# output(crawler_data,llm_data)


# def final_output(crawler_result, llm_result):
#     print("crawler data ---",crawler_result)
#     print(type(crawler_result))
#     print("llm ----",llm_result)
#     print(type(llm_result))
   
#     vendor_data = {}

#     for company_info in crawler_result:
#         company_name = company_info['company_name']
#         if company_name not in vendor_data:
#             vendor_data[company_name] = {
#                 'vendor_name': company_name,
#                 'cost': 'N/A',
#                 'time': 'N/A',
#                 'certification': 'N/A',
#                 'annual_revenue': 'N/A'
#             }

#     for vendor_info in llm_result:
#         vendor_name = vendor_info['vendor_name']
#         if vendor_name in vendor_data:
#             vendor_data[vendor_name].update(vendor_info)

#     result_list = list(vendor_data.values())
#     print(result_list)
#     return result_list

# # final_output(extract_data_crawl, list_dict)





