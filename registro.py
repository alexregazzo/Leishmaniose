from __future__ import annotations
import typing
from database import Database
import os
import logging
from datetime import datetime
import utils


class Registro:
    def __init__(self, **kwargs):
        self.reg_id = None
        self.reg_ra = None
        self.reg_nome_animal = None
        self.reg_quadra = None
        self.reg_situacao_coleta = None
        self.reg_data_coleta = None
        self.reg_teste_data_exame = None
        self.reg_teste_resultado = None
        self.reg_data_adicionado = None

        self.__dict__.update({f"reg_{dado['nome']}": kwargs[f"reg_{dado['nome']}"] for dado in utils.get_data()})

    def __getitem__(self, item):
        return self.__dict__.get(item, None)

    def toDict(self):
        return self.__dict__

    @classmethod
    def get_all(cls, *, desc=False) -> typing.List[Registro]:
        query = f"""SELECT * FROM `registro`{' ORDER BY `reg_data_adicionado` DESC' if desc else ''};"""
        with Database() as db:
            return [cls(**reg) for reg in db.select(query)]

    @classmethod
    def get_ids(cls, reg_ids, *, desc=False) -> typing.List[Registro]:
        query = f"""SELECT * FROM `registro` WHERE `reg_id` in ({", ".join([f"'{reg_id}'" for reg_id in reg_ids])}){' ORDER BY `reg_data_adicionado` DESC' if desc else ''};"""
        with Database() as db:
            return [cls(**reg) for reg in db.select(query)]

    @classmethod
    def new(cls, **kwargs) -> Registro:
        """
        :param kwargs: , reg_ra, reg_nome_animal, reg_quadra, reg_situacao_coleta, reg_data_coleta, reg_teste_data_exame, reg_teste_resultado
        """
        reg_data_adicionado = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dados = utils.get_data()
        query = f"""
        INSERT INTO registro
        ({",".join([f"`reg_{dado['nome']}`" for dado in dados if dado["coletar"] is not None])}, `reg_data_adicionado`)
        VALUES
        ({", ".join(["'%s'" % kwargs[f"reg_{dado['nome']}"] for dado in dados if dado["coletar"] is not None])}, '{reg_data_adicionado}');
        """
        try:
            with Database() as db:
                reg_id = db.insert(query)
            return cls(reg_id=reg_id, **kwargs, reg_data_adicionado=reg_data_adicionado)
        except Exception as e:
            logger.exception(e)
            raise

    @classmethod
    def update(cls, **kwargs) -> None:
        """
        :param kwargs: reg_id, reg_ra, reg_nome_animal, reg_quadra, reg_situacao_coleta, reg_data_coleta, reg_teste_data_exame, reg_teste_resultado
        """
        reg_id = kwargs["reg_id"]
        dados = utils.get_data()
        query = f"""
            UPDATE registro SET 
            {",".join([f"`reg_{dado['nome']}` = '%s'" % kwargs[f"reg_{dado['nome']}"] for dado in dados if dado["coletar"] is not None])}
            WHERE 
            `reg_id` = '{reg_id}'
            """

        print(query)

        with Database() as db:
            db.update(query)

    def __repr__(self):
        return f"<Registro {self.reg_id} {self.brief()}>"

    def brief(self):
        return f"""{self.reg_ra} {self.reg_nome_animal}"""


CURRENT_DIRPATH = os.path.dirname(__file__)
LOG_DIRPATH = "log"
LOG_NAME = os.path.splitext(os.path.split(__file__)[1])[0]
os.makedirs(os.path.join(CURRENT_DIRPATH, LOG_DIRPATH), exist_ok=True)
filepath = os.path.join(CURRENT_DIRPATH, LOG_DIRPATH, F"{LOG_NAME}.log")
LOG_FORMAT = "%(asctime)s - %(levelname)s :: %(name)s %(lineno)d :: %(message)s"
logger = logging.getLogger(LOG_NAME)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(filepath, "w", encoding='utf-8')
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(fh)
logger.propagate = False

if __name__ == "__main__":
    import json

    print(json.dumps(Registro.get_all(), default=lambda x: x.toDict()))
