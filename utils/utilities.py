import os 

def log(key: str, value: str | None = None):
    if os.getenv("print") == "true":
        print("-------------------------------------------------------------------------")
        print(key, " : ", value)
        print("=========================================================================")
