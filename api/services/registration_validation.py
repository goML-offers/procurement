import pdfrw
import sys
sys.path.insert(0, 'LLM policy generator\\api\\')
from services.send_email import send_email_with_attachment
from PyPDF2 import PdfReader


keys_to_check = [
 'date', 
 'company name', 
 'website', 
 'contact name', 
 'email', 
 'phone number', 
 'Address line 1', 
 'city', 
 'state', 
 'pincode', 
 'country', 
 'products', 
 'services', 
 'time_line'
 ] 

def extract_empty_field_names(pdf_path):
    infile = pdf_path

    pdf_reader = PdfReader(open(infile, "rb"))

    dictionary = pdf_reader.get_form_text_fields() # returns a python dictionary
    # print(dictionary)
    return dictionary

def registration_validation(input_pdf_path,mail_id):
    unfilled_values = []
    filled_values = []
    empty_fields = extract_empty_field_names(input_pdf_path)
    # print(empty_fields)
    new_dict = {key: value for key, value in empty_fields.items() if value is not None}
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
        # print("The following fields are empty:")
        # print(unfilled_values)
        message_body = f"Dear Client,\n\nWe noticed that the following fields are missing in your registration form:\n\n{', '.join(unfilled_values)}.\n\nPlease ensure to provide all the required information so that we can proceed with your registration process.\n\nThank you.\n\nSincerely,\nYour Company Name"
        subject = "Registration details update"
        send_email_with_attachment(subject,message_body,mail_id, input_pdf_path)
        return None
    else:
        # print("All fields are filled.")
        message_body = f"Hello,\n\nWe are writing to inform you that your registration has been successfully completed. Thank you for joining our community! If you have any questions or need assistance, feel free to contact our support team.\n\nBest regards,\nYour Company Name"
        subject = "Registration details update"
        send_email_with_attachment(subject,message_body,mail_id, input_pdf_path)
    return new_dict



