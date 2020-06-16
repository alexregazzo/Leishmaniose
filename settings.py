import os

DEVELOPMENT = False
ROOT_DIRPATH = os.path.dirname(__file__)
LOG_DIRPATH = os.path.join(ROOT_DIRPATH, "log")
ZIP_DIRPATH = os.path.join(ROOT_DIRPATH, "zips")
REPORT_DIRPATH = os.path.join(ROOT_DIRPATH, "relatorio")

LOG_FORMAT = "%(asctime)s - %(levelname)s :: %(name)s %(lineno)d :: %(message)s"

os.makedirs(LOG_DIRPATH, exist_ok=True)
os.makedirs(ZIP_DIRPATH, exist_ok=True)
os.makedirs(REPORT_DIRPATH, exist_ok=True)
