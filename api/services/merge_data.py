# Sample dictionaries

# rfp_list = [
#         {
#     'RFP no': '12345',
#     'RFP date': '2023-08-15',
#     'Request proposal document for ': 'IT Services',
#     'company name': 'ABC Corporation',
#     'phone number': '+1 (555) 123-4567',
#     'email id': 'info@abccorp.com',
#     'website': 'https://www.abccorp.com',
#     'last date for submission': '2023-09-30',
#     'date of opening': '2023-10-10',
#     'time of opening': '10:00 AM',
#     'signature date': '2023-08-20',
#     'chief officer signature': 'John Doe',
#     'address': '123 Main Street, Anytown, USA',
#     'introduction': 'This request for proposal (RFP) is issued to invite proposals for IT services.',
#     'scope of the work': 'The scope includes software development, system integration, and maintenance.',
#     'guideline for the biders': 'Bidders must follow the guidelines provided in the RFP document.',
#     'Technical requirements ': 'The solution must be compatible with Windows and Linux environments.',
#     'Data preprocessing or Research and development': 'Data preprocessing is a critical part of the project.',
#     'model development': 'Machine learning models will be developed for predictive analytics.',
#     'integration': 'Integration with existing systems is required.',
#     'user interface and experience ': 'A user-friendly interface is essential for this project.',
#     'Evaluation metrics': 'Performance will be evaluated based on accuracy, speed, and reliability.',
#     'timeline': 'The project is expected to be completed within 12 months.',
#     'security and privacy': 'Data security and privacy are top priorities for this project.',
#     'deployment and maintenance': 'Ongoing maintenance and support will be needed after deployment.',
#     'scalability and performance': 'The solution must be scalable to handle increased workloads.',
#     'additional notes': 'Any additional information or requirements can be found in the RFP document.',
#     'budget requirements': '$1,000,000'
# },{
#     'RFP no': 'RFQ2023-6789',
#     'RFP date': '2023-09-15',
#     'Request proposal document for ': 'Construction Services',
#     'company name': 'XYZ Builders Inc.',
#     'phone number': '+1 (555) 789-1234',
#     'email id': 'info@xyzbuilders.com',
#     'website': 'https://www.xyzbuilders.com',
#     'last date for submission': '2023-10-31',
#     'date of opening': '2023-11-15',
#     'time of opening': '2:00 PM',
#     'signature date': '2023-09-20',
#     'chief officer signature': 'Jane Smith',
#     'address': '456 Oak Street, Constructionville, USA',
#     'introduction': 'This RFP solicits proposals for a construction project for a new office building.',
#     'scope of the work': 'Scope includes architectural design, construction, and interior finishing.',
#     'guideline for the biders': 'Bidders must adhere to safety and quality standards outlined in the RFP.',
#     'Technical requirements ': 'Construction materials must meet local building codes and standards.',
#     'Data preprocessing or Research and development': 'Not applicable to this construction project.',
#     'model development': 'Architectural and structural models will be developed prior to construction.',
#     'integration': 'Integration of various construction phases is crucial for project success.',
#     'user interface and experience ': 'Focus is on functionality and safety, not a user interface.',
#     'Evaluation metrics': 'Performance will be evaluated based on project milestones and quality standards.',
#     'timeline': 'Construction is expected to be completed within 18 months.',
#     'security and privacy': 'Security measures will be in place to protect the construction site.',
#     'deployment and maintenance': 'Maintenance after construction completion will be minimal.',
#     'scalability and performance': 'Not applicable to construction services.',
#     'additional notes': 'Interested bidders should attend a pre-proposal meeting on 2023-10-05.',
#     'budget requirements': '$5,000,000'
# }
#  ]

# reg_list = [
#         {'to address': 'Neural go', 'Quote date': '21/08/2023', 'Quote number': '1', 'customer id': '123', 'valid until': '09/09/2023', 'company name': 'ABC Corporation', 'name': 'Akash', 'address': 'Coimbatore', 'email': 'csakash03@gmail.com', 'phone': '12345', 'sign date': '21/08/2023', 'signature ': 'Akash', 'item 1': '1', 'sub total': '1080', 'tax': '10%', 'tax rate': '108', 'shipping price': '100', 'total 1': '1080', 'discount 1': '10', 'unit price 1': '1200', 'quantity  1': '1', 'description 1': 'computer'},
#         {'to address': 'Neural go', 'Quote date': '21/08/2023', 'Quote number': '1', 'customer id': '123', 'valid until': '09/09/2023', 'company name': 'XYZ Builders Inc.', 'name': 'Akash', 'address': 'Coimbatore', 'email': 'csakash03@gmail.com', 'phone': '12345', 'sign date': '21/08/2023', 'signature ': 'Akash', 'item 1': '1', 'sub total': '1080', 'tax': '10%', 'tax rate': '108', 'shipping price': '100', 'total 1': '1080', 'discount 1': '10', 'unit price 1': '1200', 'quantity  1': '1', 'description 1': 'computer'}

# ]

# Merge dictionaries based on company_name it has rfp_list and reg_list
def merge_by_company_name(rfp_list,reg_list):
   
    merged_dict = {}
    for rfp in rfp_list:
        merged_dict[rfp['company name']] = [rfp,None]
        
    for proposal in reg_list:
        if proposal['company name'] in merged_dict:
            merged_dict[proposal['company name']][1] = proposal
        else:
            merged_dict[proposal['company name']] = [ None,
                                                proposal ]

    merged_dict = str(merged_dict)
    print(merged_dict)
    return merged_dict

    
    
