from dotenv import load_dotenv
import os

load_dotenv()

def getKey():
    return os.getenv("ADA_KEY")

def getUsername():
    return os.getenv("ADA_USERNAME")