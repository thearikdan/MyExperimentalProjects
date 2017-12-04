import os.path

def get_company_name_from_file_name(filename):
    name_ext = os.path.basename(filename)  
    name = os.path.splitext(name_ext)[0]
    return name
