import os
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    SECRET_KEY = os.getenv("SECRETKEY")
    