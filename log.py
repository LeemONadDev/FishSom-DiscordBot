from datetime import datetime

class Log:
    def time(self):
        return datetime.now()

def log(time="",type="",content=""):
    print(f"[{time}] [{type}] {content}")