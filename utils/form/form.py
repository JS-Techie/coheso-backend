import os, json

from schemas.form import FormDataRequestBody

class Form:
    
    def read_form_db(self) -> (any, any): # type: ignore
        try:
            with open(os.getenv('DB_FILE'), 'r') as f:
                return (json.load(f)['forms'], '')
        except Exception as e:
            return ([], str(e))
        

    def append_form_db(self, forms) -> (any, any):  # type: ignore
        try:
            with open(os.getenv('DB_FILE'), 'r') as f:
                existing_data = json.load(f)
            
            forms_json_serializable = []
            for form in forms:
                forms_json_serializable.append(form.dict() if hasattr(form, 'dict') else form)
            existing_data['forms'].extend(forms_json_serializable)
            with open(os.getenv('DB_FILE'), 'w') as f:
                json.dump(existing_data, f, indent=6)
            return "file write successful", []
        except Exception as e:
            return [], str(e)
                
    def write_form_db(self, forms) -> (any, any):  # type: ignore
        try:
            with open(os.getenv('DB_FILE'), 'r') as f:
                existing_data = json.load(f)
            
            forms_json_serializable = []
            for form in forms:
                forms_json_serializable.append(form.dict() if hasattr(form, 'dict') else form)
            existing_data['forms']=forms_json_serializable
            with open(os.getenv('DB_FILE'), 'w') as f:
                json.dump(existing_data, f, indent=6)
            return "file write successful", []
        except Exception as e:
            return [], str(e)
    