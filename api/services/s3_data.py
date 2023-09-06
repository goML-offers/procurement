import json
import boto3
from boto3.session import Session
import os
from dotenv import load_dotenv
load_dotenv()

# AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID_S3")
# AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY_S3")



# session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
# aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
# s3 = session.resource('s3')
# s3_client = s3.Bucket('gomloffers')
os.environ['AWS_ACCESS_KEY_ID'] = "AKIA3OBOBB2KAPCAI5EE"

os.environ['AWS_SECRET_ACCESS_KEY'] = "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"

 

 

 

session = Session(aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],

aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

s3 = session.resource('s3')

s3_client = s3.Bucket('gomloffers')

# s3_client.upload_file(Key="procurement/rfp_Saigon_Technology.pdf", Filename = "C:\\Users\\Hxtreme\\OneDrive - Neuralgo\\Desktop\\model rfpSaigon Technology.pdf")
# s3_client.download_file(Key="procurement/registration_form_saigontechnology.pdf", Filename = "registration_form_saigontechnology.pdf")
# for file in s3_client.objects.all():
#     print(file.key)
"""
# session = boto3.Session(
#     aws_access_key_id='AKIA3Q5RVG3GBETDPL46',
#     aws_secret_access_key='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'
# )

# Initialize the S3 client using the session
# s3 = session.client('s3')

# bucket_name = 'goml-offers'


# Initialize the S3 client
# s3 = boto3.client('s3')



# Create the folder (prefix) in the S3 bucket


file_path = 'data.txt'
local_file_path = file_path
# Define the file path where you want to save the data"""
def push_to_s3(file_path,company_name):
    print(file_path)
    folder_name = company_name
    file_name = file_path.split('/')[-1]
    print(file_name)
    # s3_client.put_object(Bucket="gomloffers", Key="procurement/")
    # s3_client.put_object(Bucket="gomloffers", Key=f'procurement/{folder_name}/')
    # Upload the text file to the S3 folder
    s3_key = "procurement/"+folder_name+"/"+file_name
    s3_client.upload_file(Key=s3_key, Filename=file_path)
    # s3_client.upload_file(Key="procurement"+f'{folder_name}/{file_name}', Filename = file_path)
    os.remove(file_path)
   
    return s3_key
# push_to_s3('C:\\Users\\Hxtreme\\OneDrive - Neuralgo\\Desktop\\model rfpSaigon Technology.pdf', 'model rfpSaigon Technology.pdf')
# print(f'List of dictionaries has been saved to {file_path}')


def get_from_s3(s3_path):
    file_name=s3_path.split('/')[-1]
    s3_client.download_file(Key=s3_path, Filename = file_name)
    return file_name
