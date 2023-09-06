# import json
# import boto3
# import os
# from dotenv import load_dotenv
# load_dotenv()
# folder_path = os.getenv("FOLDER_PATH")

# # Define the file path where you want to save the data
# def push_to_local(data_list, company_name):
#     folder_path_new = os.path.join(folder_path, company_name)
#     file_path = os.path.join(folder_path_new, "data.txt")  # Updated file name, removing the dot (.)
    
#     try:
#         # Create the directory structure if it doesn't exist
#         if not os.path.exists(folder_path_new):
#             os.makedirs(folder_path_new)
        
#         with open(file_path, 'w') as file:
#             json.dump(data_list, file, indent=4)  # Changed 'data' to 'data_list' to match the function argument
#         print(f"Data saved to {file_path} successfully.")
#     except Exception as e:
#         print(f"An error occurred while saving data: {str(e)}")

# def get_from_local(company_name):
#     folder_path_new = os.path.join(folder_path, company_name)
#     file_path = os.path.join(folder_path_new, "data.txt")
    
#     # Initialize an empty list to store the extracted dictionaries
#     extracted_data_list = []

#     try:
#         # Open the file in read mode and load the JSON data
#         with open(file_path, 'r') as file:
#             extracted_data_list = json.load(file)
#         print("Data loaded successfully.")
#     except FileNotFoundError:
#         print(f"File '{file_path}' not found.")
#     except json.JSONDecodeError as e:
#         print(f"Error decoding JSON data: {e}")
    
#     # Remove the folder and its contents
#     try:
#         os.remove(file_path)  # Remove the 'data.txt' file
#         os.rmdir(folder_path_new)  # Remove the folder
#         # print(f"Folder '{folder_path_new}' and its contents removed.")
#     except FileNotFoundError:
#         return f"Folder '{folder_path_new}' not found."
    
#     # Now 'extracted_data_list' contains the list of dictionaries from the file
#     return extracted_data_list
