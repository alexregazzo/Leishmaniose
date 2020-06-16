from __future__ import annotations
import typing
from database import Database
import database.utils
from datetime import datetime
import utils


class Registro:
    def __init__(self, **kwargs):
        self.reg_id = None
        self.reg_ra = None
        self.reg_nome_animal = None
        self.reg_nome_dono = None
        self.reg_endereco = None
        self.reg_quadra = None
        self.reg_situacao_coleta = None
        self.reg_data_coleta = None
        self.reg_teste_data_exame = None
        self.reg_teste_resultado = None
        self.reg_data_adicionado = None

        self.__dict__.update({f"reg_{dado['nome']}": kwargs[f"reg_{dado['nome']}"] for dado in utils.get_data()})

    def __getitem__(self, item):
        return self.__dict__.get(item, None)

    def json(self):
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
        sql = database.utils.make_insert(*[f"reg_{dado['nome']}" for dado in utils.get_data() if dado["coletar"] is not None], "reg_data_adicionado", t_name="registro")
        try:
            with Database() as db:
                reg_id = db.insert(sql, **kwargs, reg_data_adicionado=reg_data_adicionado)
            return cls(reg_id=reg_id, **kwargs, reg_data_adicionado=reg_data_adicionado)
        except Exception as e:
            logger.exception(e)
            raise

    @staticmethod
    def update(**kwargs) -> None:
        """
        :param kwargs: reg_id, reg_ra, reg_nome_animal, reg_quadra, reg_situacao_coleta, reg_data_coleta, reg_teste_data_exame, reg_teste_resultado
        """
        sql = database.utils.make_update(set_list=[f"reg_{dado['nome']}" for dado in utils.get_data() if dado["coletar"] is not None], where_list=["reg_id"], t_name="registro")
        with Database() as db:
            db.update(sql, **kwargs)

    @staticmethod
    def delete(**kwargs) -> None:
        sql = database.utils.make_delete("reg_id", t_name="registro")
        with Database() as db:
            db.delete(sql, **kwargs)

    def __repr__(self):
        return f"<Registro {self.reg_id} {self.brief()}>"

    def brief(self):
        return f"""{self.reg_ra} {self.reg_nome_animal}"""


logger = utils.get_logger(__file__)

if __name__ == "__main__":
    pass
