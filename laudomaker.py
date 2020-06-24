import docx
import os
import registro
import typing
import utils
import settings
import re


def make_laudos(regs: typing.List[registro.Registro]) -> typing.List[str]:
    logger.debug(f"Generate laudos from {regs}")
    dados = utils.get_data()
    results = []
    for reg in regs:
        doc = docx.Document(os.path.join(settings.ROOT_DIRPATH, "laudo.docx"))
        formatter = {dado["laudo"]: reg[f"reg_{dado['nome']}"] if dado["tipo"] != "date" else utils.strstd2strusr(reg[f"reg_{dado['nome']}"]) for dado in dados if dado["laudo"] is not None}
        for p in doc.paragraphs:
            if re.findall("{\w+}", p.text):
                p.text = p.text.format(**formatter)
        fpath = utils.make_unique_filepath(os.path.join(settings.LAUDO_DIRPATH, make_filename(reg=reg) + ".docx"))
        doc.save(fpath)
        logger.debug(f"Laudo file save as: {fpath}")
        results.append(fpath)
    return results


def make_filename(*, reg: registro.Registro) -> str:
    return utils.get_datetime_for_file() + "_RA" + reg.reg_ra


logger = utils.get_logger(__file__)
if __name__ == "__main__":
    pass
