import pdfrw
import sys
import os 
sys.path.insert(0, 'LLM policy generator\\api\\')
from services.send_email import send_email_with_attachment
from PyPDF2 import PdfReader
keys_to_check = [   
 'to address', 
 'Quote date', 
 'Quote number', 
 'customer id', 
 'valid until', 
 'company name', 
 'name', 'address', 
 'email', 
 'phone', 
 'sign date', 
 'signature ', 
 'item 1', 
 'sub total', 
 'tax', 
 'tax rate', 
 'shipping price', 
 'total 1', 
 'discount 1', 
 'unit price 1', 
 'quantity  1',
 'description 1']

def extract_empty_field_names(pdf_path):
    infile = pdf_path
    with open(pdf_path, "rb") as infile:
        pdf_reader = PdfReader(infile)

        dictionary = pdf_reader.get_form_text_fields() # returns a python dictionary
    
    
    return dictionary

def rfp_validation(input_pdf_path,mail_id):

    unfilled_values = []
    filled_values = []
    empty_fields = extract_empty_field_names(input_pdf_path)

    new_dict = {key: value for key, value in empty_fields.items() if value is not None}
    print(new_dict)
    for key, value in empty_fields.items():
        key = str(key)
        if type(value)!=None:
            value = str(value)
        if (value == "None" or value == ""):
            
            if key in keys_to_check:
                unfilled_values.append(key)
        else:
            filled_values.append(key)
    if unfilled_values: 
        print("1")
        # print("The following fields are empty:")
        # print(unfilled_values)
        message_body = f"Dear Client,\n\nWe noticed that the following fields are missing in your registration form:\n\n{', '.join(unfilled_values)}.\n\nPlease ensure to provide all the required information so that we can proceed with your registration process.\n\nThank you.\n\nSincerely,\nYour Company Name"
        subject = "Registration details update"
        send_email_with_attachment(subject,message_body,mail_id, input_pdf_path)
        return None
    else:
        print("2")
        # print("All fields are filled.")
        message_body = f"Hello,\n\nWe are writing to inform you that your registration has been successfully completed. Thank you for joining our community! If you have any questions or need assistance, feel free to contact our support team.\n\nBest regards,\nYour Company Name"
        subject = "Registration details update"
        send_email_with_attachment(subject,message_body,mail_id, input_pdf_path)
    return new_dict

def rfp_data_extraction(file_path):
    # print("fp",file_path)
    empty_fields = extract_empty_field_names(file_path)
    new_dict = {key: value for key, value in empty_fields.items() if value is not None}
    os.remove(file_path)
    return new_dict
# 'RFP no',
    # 'RFP date', 
    # 'Request proposal document for ', 
    # 'company name', 
    # 'phone number', 
    # 'email id', 
    # 'website', 
    # 'last date for submission', 
    # 'date of opening', 
    # 'time of opening', 
    # 'signature date', 
    # 'chief officer signature', 
    # 'address', 
    # 'introduction', 
    # 'scope of the work', 
    # 'guideline for the biders', 
    # 'Technical requirements ', 
    # 'Data preprocessing or Research and development', 
    # 'model development', 
    # 'integration', 
    # 'user interface and experience ', 
    # 'Evaluation metrics', 
    # 'timeline', 
    # 'security and privacy', 
    # 'deployment and maintenance', 
    # 'scalability and performance', 
    # 'additional notes', 
    # 'budget requirements'