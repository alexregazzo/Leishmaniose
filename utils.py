import json
import os
import logging
import settings
from datetime import datetime
from zipfile import ZipFile
import typing


def get_data() -> dict:
    dados_path = os.path.join(CURRENT_DIRPATH, "dados.json")
    logger.debug(f"Data path: {dados_path}")
    try:
        with open(dados_path, encoding="utf8") as f:
            return json.load(f)
    except Exception as e:
        logger.critical("A problem ocurred while trying to get data from data file")
        logger.exception(e)
        raise


def get_logger(path: str, LOG_NAME: str = None, propagate: bool = False) -> logging.Logger:
    if LOG_NAME is None:
        LOG_NAME = os.path.splitext(os.path.relpath(path, settings.ROOT_DIRPATH).replace("\\", "_").replace("/", "_"))[0] + ".log"
    logger_maker = logging.getLogger(LOG_NAME)
    if os.path.splitext(LOG_NAME)[1] != ".log":
        LOG_NAME += ".log"
    filepath = os.path.join(settings.LOG_DIRPATH, LOG_NAME)
    logger_maker.setLevel(logging.DEBUG)
    fh = logging.FileHandler(filepath, "w" if settings.DEVELOPMENT else "a", encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(settings.LOG_FORMAT))
    logger_maker.addHandler(fh)
    logger_maker.propagate = propagate
    return logger_maker


def make_unique_filepath(fpath: str) -> str:
    logger.debug(f"Path checking: {fpath}")
    if os.path.exists(fpath):
        fname, fext = os.path.splitext(fpath)
        fpath = fname + "_({})" + fext
        k = 0
        while os.path.exists(fpath.format(k)):
            k += 1
        fpath = fpath.format(k)
    else:
        logger.debug("Path doesn't exist")
    logger.debug(f"Path name is: {fpath}")
    return fpath


def strstd2strusr(datestr: str) -> str:
    try:
        d = datetime.strptime(datestr, "%Y-%m-%d")
    except ValueError:
        return datestr
    else:
        return d.strftime("%d/%m/%Y")


def get_datetime_for_file() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def zip_files(files: typing.List[str], *, remove_dirs: bool = False) -> str:
    logger.debug(f"Zipping files: {files}")
    zippath = make_unique_filepath(os.path.join(settings.ZIP_DIRPATH, get_datetime_for_file() + '.zip'))
    logger.debug(f"Zip started")
    with ZipFile(zippath, 'w') as myzip:
        for file in files:
            logger.debug(f"Writing file {file}")
            myzip.write(file, arcname=(os.path.split(file)[1] if remove_dirs else None))
            logger.debug(f"Success")
    return zippath


CURRENT_DIRPATH = os.path.dirname(__file__)
logger = get_logger(__file__)
