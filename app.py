from flask import Flask, render_template, request, Response, send_file, url_for
from werkzeug.utils import secure_filename
import os
from registro import Registro
import utils
import json
from datetime import datetime
import sheetmaker
import planilha
import settings

app = Flask(__name__)


@app.route('/')
def page_resumo():
    return render_template("resumo.html")


@app.route("/planilha")
def page_planilha():
    return render_template("planilha.html")


@app.route("/busca")
def page_busca():
    return render_template("busca.html")


@app.route("/registro")
def page_registro():
    return render_template("registro.html")


@app.route("/gerar_relatorio")
def page_gerar_relatorio():
    return render_template("relatorio.html")


@app.route("/relatorios_antigos")
def page_relatorios_antigos():
    return render_template("relatorios_antigos.html")


@app.route('/adicionar')
def page_adicionar_registro():
    return render_template("registrar.html")


@app.route("/api/registros")
def api_get():
    filtro_id = request.args.get("filtro_id", "")
    filtro_ra = request.args.get("filtro_ra", "")
    filtro_nome_animal = request.args.get("filtro_nome_animal", "")
    filtro_nome_dono = request.args.get("filtro_nome_dono", "")
    filtro_endereco = request.args.get("filtro_endereco", "")
    filtro_quadra = request.args.get("filtro_quadra", "")
    filtro_situacao_coleta = request.args.get("filtro_situacao_coleta", "")
    filtro_data_col_inicio = request.args.get("filtro_data_col_inicio", "")
    filtro_data_col_fim = request.args.get("filtro_data_col_fim", "")
    filtro_data_exa_inicio = request.args.get("filtro_data_exa_inicio", "")
    filtro_data_exa_fim = request.args.get("filtro_data_exa_fim", "")
    filtro_teste_resultado = request.args.get("filtro_teste_resultado", "")
    filtro_data_add_inicio = request.args.get("filtro_data_add_inicio", "")
    filtro_data_add_fim = request.args.get("filtro_data_add_fim", "")

    regs = Registro.get_all(desc=request.args.get("desc", None) is not None)
    results = []
    try:
        for reg in regs:
            logger_filter.debug(reg)
            if filtro_id != "" and str(reg.reg_id) != filtro_id:
                logger_filter.debug("Filtered by id")
                continue
            if filtro_ra != "" and reg.reg_ra != filtro_ra:
                logger_filter.debug("Filtered by ra")
                continue
            if filtro_nome_animal != "" and filtro_nome_animal not in reg.reg_nome_animal:
                logger_filter.debug("Filtered by nome animal")
                continue
            if filtro_nome_dono != "" and filtro_nome_dono in reg.reg_nome_dono:
                logger_filter.debug("Filtered by nome dono")
                continue
            if filtro_endereco != "" and filtro_endereco in reg.reg_endereco:
                logger_filter.debug("Filtered by endereco")
                continue
            if filtro_quadra != "" and reg.reg_quadra != filtro_quadra:
                logger_filter.debug("Filtered by quadra")
                continue
            if filtro_situacao_coleta != "" and reg.reg_situacao_coleta != filtro_situacao_coleta:
                logger_filter.debug("Filtered by situação coleta")
                continue
            if filtro_data_col_inicio != "" and not datetime.strptime(reg.reg_data_coleta, "%Y-%m-%d").date() >= datetime.strptime(filtro_data_col_inicio, "%Y-%m-%d").date():
                logger_filter.debug("Filtered by data coleta inicio")
                continue
            if filtro_data_col_fim != "" and not datetime.strptime(reg.reg_data_coleta, "%Y-%m-%d").date() <= datetime.strptime(filtro_data_col_fim, "%Y-%m-%d").date():
                logger_filter.debug("Filtered by data coleta fim")
                continue
            if filtro_data_exa_inicio != "" and not datetime.strptime(reg.reg_teste_data_exame, "%Y-%m-%d").date() >= datetime.strptime(filtro_data_exa_inicio, "%Y-%m-%d").date():
                logger_filter.debug("Filtered by teste data exame inicio")
                continue
            if filtro_data_exa_fim != "" and not datetime.strptime(reg.reg_teste_data_exame, "%Y-%m-%d").date() <= datetime.strptime(filtro_data_exa_fim, "%Y-%m-%d").date():
                logger_filter.debug("Filtered by teste data exame fim")
                continue
            if filtro_teste_resultado != "" and reg.reg_teste_resultado != filtro_teste_resultado:
                logger_filter.debug("Filtered by teste resultado")
                continue
            if filtro_data_add_inicio != "" and not datetime.strptime(reg.reg_data_adicionado, "%Y-%m-%d %H:%M:%S").date() >= datetime.strptime(filtro_data_add_inicio, "%Y-%m-%d").date():
                logger_filter.debug("Filtered by data adicionado")
                continue
            if filtro_data_add_fim != "" and not datetime.strptime(reg.reg_data_adicionado, "%Y-%m-%d %H:%M:%S").date() <= datetime.strptime(filtro_data_add_fim, "%Y-%m-%d").date():
                continue
            results.append(reg)
    except Exception as e:
        logger.debug(request.args.to_dict())
        logger.exception(e)
        return Response(response=json.dumps([]), status=400, mimetype="application/json")
    else:
        return Response(response=json.dumps(results, default=lambda x: x.json()), status=200, mimetype="application/json")


@app.route('/api/dados')
def api_dados():
    try:
        return json.dumps(utils.get_data())
    except Exception as e:
        logger.exception(e)
        logger.debug("Returning empty list")
        return Response(response=json.dumps([]), status=400, mimetype="application/json")


@app.route('/api/registrar', methods=["POST"])
def api_registrar():
    try:
        logger.debug(f"Request of register: {request.form}")
        reg = Registro.new(**{f"reg_{dado['nome']}": request.form[f"reg_{dado['nome']}"] for dado in utils.get_data() if dado["coletar"]})
    except KeyError as e:
        logger.exception(e)
        return Response(response=f"Erro ao adicionar registro, dados insuficientes", status=400)
    except Exception as e:
        logger.exception(e)
        return Response(response=f"Erro ao adicionar registro", status=400)
    else:
        logger.debug("Register success")
        return Response(response=f"""Adicionado com sucesso: '{reg.brief()}'""", status=201)


@app.route('/api/gerar_relatorio', methods=["POST"])
def api_gen_relatorio():
    logger.debug(f"Generate report: {request.form}")
    try:
        fpath = sheetmaker.zip_files(sheetmaker.make_sheet(regs=Registro.get_ids(request.form.getlist("reg_ids"))), remove_dirs=True)
    except Exception as e:
        logger.exception(e)
        return ""
    else:
        return url_for("api_get_relatorio", fname=os.path.split(fpath)[1])


@app.route('/api/relatorio/<string:fname>')
def api_get_relatorio(fname: str):
    fp = os.path.join(settings.ZIP_DIRPATH, secure_filename(fname))
    logger.debug(f"Get zip file: {fp}")
    if os.path.isfile(fp):
        logger.debug(f"File found")
        return send_file(fp, mimetype="application/zip")
    else:
        logger.debug(f"File not found")
        return Response(status=404)


@app.route('/api/relatorios_antigos')
def api_relatorios_antigos():
    logger.debug(f"Old reports:")
    try:
        reports_paths = [url_for("api_get_relatorio", fname=report_path) for report_path in os.listdir(settings.ZIP_DIRPATH)]
    except Exception as e:
        logger.exception(e)
        return Response(response=json.dumps([]), status=400)
    else:
        logger.debug(f"Success: {reports_paths}")
        return Response(response=json.dumps(reports_paths), status=200)


@app.route('/api/atualizar', methods=["POST"])
def api_update_registro():
    # post request
    logger.debug(f"Update: {request.form}")
    try:
        Registro.update(**request.form)
    except Exception as e:
        logger.exception(e)
        return Response(status=400)
    else:
        logger.debug("Success")
        return Response(status=200)


@app.route('/api/delete', methods=["POST"])
def api_delete_registro():
    # post request
    logger.debug(f"Delete: {request.form}")
    try:
        Registro.delete(**request.form)
    except Exception as e:
        logger.exception(e)
        return Response(response="Erro ao deletar registro", status=400)
    else:
        logger.debug("Success")
        return Response(response="Registro deletado com sucesso", status=200)


@app.route('/api/get_data_from_spreadsheet', methods=["POST"])
def api_get_data_from_spreadsheet():
    # post request
    logger.debug("Get data from spreadsheet")
    try:
        records = planilha.get_new_records()
        dados = utils.get_data()
    except Exception as e:
        logger.exception(e)
        return Response(response="Erro ao processar planilha", status=400)
    else:
        logger.debug("Success")
        return Response(response=json.dumps({"dados": dados, "registros": records}, default=lambda x: x.json()), status=200)


@app.route('/api/delete_inserted_data_from_spreadsheet', methods=["POST"])
def api_delete_inserted_data_from_spreadsheet():
    # post request
    logger.debug("Delete data from spreadsheet")
    try:
        planilha.delete_inserted_data()
    except Exception as e:
        logger.exception(e)
        return Response(response="Erro ao deletar dados da planilha", status=400)
    else:
        logger.debug("Success")
        return Response(response="Dados deletados com sucesso", status=200)


logger = utils.get_logger(__file__)
logger_filter = utils.get_logger(__file__, LOG_NAME="filter-log")

if __name__ == '__main__':
    import platform

    if platform.system() == "Windows":
        # app.run(host="127.0.0.1", port=5000, debug=True)
        app.run(host="0.0.0.0", port=5000, debug=True)
    elif platform.system() == "Linux":
        print("Log directed to file")
        utils.get_logger(__file__, LOG_NAME="werkzeug")
        app.run(host='0.0.0.0', port=8001, debug=False)
