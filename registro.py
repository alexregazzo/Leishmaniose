from __future__ import annotations
import typing
from database import Database
import os
import logging
from datetime import datetime


class Registro:
    def __init__(self, *,
                 reg_id,
                 reg_ra,
                 reg_nome_animal,
                 reg_endereco_nome_dono,
                 reg_quadra,
                 reg_situacao_coleta,
                 reg_data_coleta,
                 reg_teste_data_exame,
                 reg_teste_resultado,
                 reg_exame_numero_amostra,
                 reg_exame_data,
                 reg_exame_resultado,
                 reg_sintomas,
                 reg_eutanasia_realizada,
                 reg_eutanasia_data,
                 reg_data_adicionado
                 ):
        self.reg_id = reg_id
        self.reg_ra = reg_ra
        self.reg_nome_animal = reg_nome_animal
        self.reg_endereco_nome_dono = reg_endereco_nome_dono
        self.reg_quadra = reg_quadra
        self.reg_situacao_coleta = reg_situacao_coleta
        self.reg_data_coleta = reg_data_coleta
        self.reg_teste_data_exame = reg_teste_data_exame
        self.reg_teste_resultado = reg_teste_resultado
        self.reg_exame_numero_amostra = reg_exame_numero_amostra
        self.reg_exame_data = reg_exame_data
        self.reg_exame_resultado = reg_exame_resultado
        self.reg_sintomas = reg_sintomas
        self.reg_eutanasia_realizada = reg_eutanasia_realizada
        self.reg_eutanasia_data = reg_eutanasia_data
        self.reg_data_adicionado = reg_data_adicionado

    @classmethod
    def get_all(cls) -> typing.List[Registro]:
        query = """SELECT * FROM registro;"""
        with Database() as db:
            return [cls(**reg) for reg in db.select(query)]

    @classmethod
    def new(cls, *,
            reg_ra,
            reg_nome_animal,
            reg_endereco_nome_dono,
            reg_quadra,
            reg_situacao_coleta,
            reg_data_coleta,
            reg_teste_data_exame,
            reg_teste_resultado,
            reg_exame_numero_amostra,
            reg_exame_data,
            reg_exame_resultado,
            reg_sintomas,
            reg_eutanasia_realizada,
            reg_eutanasia_data
            ) -> Registro:

        reg_data_adicionado = datetime.now().strftime("%Y-%m-%d %H:%M%S")
        query = f"""INSERT INTO registro(
                reg_ra, 
                reg_nome_animal, 
                reg_endereco_nome_dono,
                reg_quadra,
                reg_situacao_coleta, 
                reg_data_coleta,
                reg_teste_data_exame, 
                reg_teste_resultado, 
                reg_exame_numero_amostra,
                reg_exame_data,
                reg_exame_resultado,
                reg_sintomas,
                reg_eutanasia_realizada,
                reg_eutanasia_data,
                reg_data_adicionado
            ) VALUES ( 
                '{reg_ra}',
                '{reg_nome_animal}',
                '{reg_endereco_nome_dono}',
                '{reg_quadra}',
                '{reg_situacao_coleta}',
                '{reg_data_coleta}',
                '{reg_teste_data_exame}',
                '{reg_teste_resultado}',
                '{reg_exame_numero_amostra}',
                '{reg_exame_data}',
                '{reg_exame_resultado}',
                '{reg_sintomas}',
                '{reg_eutanasia_realizada}',
                '{reg_eutanasia_data}',
                '{reg_data_adicionado}'
            );
        """

        try:
            with Database() as db:
                reg_id = db.insert(query)
            return cls(
                reg_id=reg_id,
                reg_ra=reg_ra,
                reg_nome_animal=reg_nome_animal,
                reg_endereco_nome_dono=reg_endereco_nome_dono,
                reg_quadra=reg_quadra,
                reg_situacao_coleta=reg_situacao_coleta,
                reg_data_coleta=reg_data_coleta,
                reg_teste_data_exame=reg_teste_data_exame,
                reg_teste_resultado=reg_teste_resultado,
                reg_exame_numero_amostra=reg_exame_numero_amostra,
                reg_exame_data=reg_exame_data,
                reg_exame_resultado=reg_exame_resultado,
                reg_sintomas=reg_sintomas,
                reg_eutanasia_realizada=reg_eutanasia_realizada,
                reg_eutanasia_data=reg_eutanasia_data,
                reg_data_adicionado=reg_data_adicionado
            )
        except Exception as e:
            logger.exception(e)
            raise

    def brief(self):
        return f"""{self.reg_ra} {self.reg_nome_animal} {self.reg_endereco_nome_dono}"""


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
