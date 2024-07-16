import os, json
from schemas.submission import SubmissionRequestBody

class Submission:
    
    def read_submission_db(self) -> (any, any): # type: ignore
        try:
            with open(os.getenv('DB_FILE'), 'r') as f:
                return (json.load(f)['submissions'], '')
        except Exception as e:
            return ([], str(e))
        

    def append_submission_db(self, submissions) -> (any, any):  # type: ignore
        try:
            with open(os.getenv('DB_FILE'), 'r') as f:
                existing_data = json.load(f)
            
            submissions_json_serializable = []
            for submission in submissions:
                submissions_json_serializable.append(submission.dict())
            existing_data['submissions'].extend(submissions_json_serializable)
            print(existing_data['submissions'])
            with open(os.getenv('DB_FILE'), 'w') as f:
                json.dump(existing_data, f, indent=6)
            return "file write successful", []
        except Exception as e:
            return [], str(e)
                
    def write_submission_db(self, submissions) -> (any, any):  # type: ignore
        try:
            with open(os.getenv('DB_FILE'), 'r') as f:
                existing_data = json.load(f)
            
            submissions_json_serializable = []
            for submission in submissions:
                submissions_json_serializable.append(submission.dict() if hasattr(submission, 'dict') else submission)
            existing_data['submissions']=submissions_json_serializable
            with open(os.getenv('DB_FILE'), 'w') as f:
                json.dump(existing_data, f, indent=6)
            return "file write successful", []
        except Exception as e:
            return [], str(e)
    