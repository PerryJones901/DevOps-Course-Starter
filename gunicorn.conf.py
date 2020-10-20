import os
from dotenv import find_dotenv, load_dotenv

file_path = find_dotenv('.env')
load_dotenv(file_path)
