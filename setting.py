from os.path import join, dirname
import os

# debug
# from dotenv import load_dotenv

# load_dotenv(verbose=True)

# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")
