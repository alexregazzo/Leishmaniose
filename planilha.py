import gspread
from google.oauth2 import service_account
import os
import utils
from registro import Registro
import typing
import logging


def get_sheet_client() -> gspread.client.Client:
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(credentials)
    return client


def create_dict_from_str_list(lista) -> dict:
    result = dict()
    for j, dado in enumerate([dado for dado in utils.get_data() if dado["coletar"]]):
        if dado["valores"] is not None:
            result[f'reg_{dado["nome"]}'] = dado["valores"].index(lista[j])
        else:
            result[f'reg_{dado["nome"]}'] = lista[j]
    return result


def get_new_records() -> typing.List[Registro]:
    try:
        logger.debug("Running get from spreadsheet")
        client = get_sheet_client()
        sheet = client.open("Leishmaniose").get_worksheet(0)
        updates = []
        added = []
        for i, row in enumerate(sheet.get_all_values()):
            if i == 0:
                continue
            if row[-1] != "":
                continue
            if row[0] == "" or row[1] == "":
                continue
            try:
                reg_dict = create_dict_from_str_list(row)
                reg = Registro.new(**reg_dict)
            except Exception as e:
                logger.exception(e)
            else:
                added.append(reg)
                updates.append({"range": "H" + str(i + 1), "values": [[reg.reg_data_adicionado]]})

        sheet.batch_update(updates)
    except Exception as e:
        logger.exception(e)
        raise
    else:
        return added


def delete_inserted_data() -> None:
    try:
        logger.debug("Running delete from spreadsheet")
        client = get_sheet_client()
        sheet = client.open("Leishmaniose").get_worksheet(0)
        CLEAR_ROW_VALUES = [["" for _ in range(sheet.col_count)]]
        removes = []
        for i, row in enumerate(sheet.get_all_values()):
            if i == 0:
                continue
            if row[-1] == "":
                continue
            removes.append({"range": f"{i + 1}:{i + 1}", "values": CLEAR_ROW_VALUES})
        sheet.batch_update(removes)
    except Exception as e:
        logger.exception(e)
        raise


CURRENT_DIRPATH = os.path.dirname(__file__)
SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = os.path.join(CURRENT_DIRPATH, 'google_service_key.json')
LOG_DIRPATH = "../log"
LOG_NAME = os.path.splitext(os.path.split(__file__)[1])[0]
os.makedirs(os.path.join(CURRENT_DIRPATH, LOG_DIRPATH), exist_ok=True)
filepath = os.path.join(CURRENT_DIRPATH, LOG_DIRPATH, F"{LOG_NAME}.log")
LOG_FORMAT = "%(asctime)s - %(levelname)s :: %(name)s %(lineno)d :: %(message)s"
logger = logging.getLogger(LOG_NAME)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(filepath, "a", encoding='utf-8')
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(fh)
logger.propagate = False

if __name__ == "__main__":
    delete_inserted_data()
