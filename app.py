from flask import Flask, render_template, request, Response, send_file, url_for
from werkzeug.utils import secure_filename
import os
from registro import Registro
import utils
import json
from datetime import datetime
import sheet_maker
import planilha

app = Flask(__name__)


@app.route('/')
def resumo_page():
    return render_template("resumo.html")


@app.route("/planilha")
def planilha_page():
    return render_template("planilha.html")


@app.route("/busca")
def busca_page():
    return render_template("busca.html")


@app.route("/registro")
def registro_page():
    return render_template("registro.html")


@app.route("/gerar_relatorio")
def gerar_relatorio_page():
    return render_template("relatorio.html")


@app.route('/adicionar')
def add_register_page():
    return render_template("adicionar.html")


@app.route("/api/registros")
def api_get():
    filtro_id = request.args.get("filtro_id", "")
    filtro_ra = request.args.get("filtro_ra", "")
    filtro_nome_animal = request.args.get("filtro_nome_animal", "")
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
            if filtro_id != "" and str(reg.reg_id) != filtro_id:
                continue
            if filtro_ra != "" and reg.reg_ra != filtro_ra:
                continue
            if filtro_nome_animal != "" and filtro_nome_animal not in reg.reg_nome_animal:
                continue
            if filtro_quadra != "" and reg["reg_quadra"] != filtro_quadra:
                continue
            if filtro_situacao_coleta != "" and reg.reg_situacao_coleta != filtro_situacao_coleta:
                continue
            if filtro_data_col_inicio != "" and not datetime.strptime(reg.reg_data_coleta, "%Y-%m-%d").date() >= datetime.strptime(filtro_data_col_inicio, "%Y-%m-%d").date():
                continue
            if filtro_data_col_fim != "" and not datetime.strptime(reg.reg_data_coleta, "%Y-%m-%d").date() <= datetime.strptime(filtro_data_col_fim, "%Y-%m-%d").date():
                continue
            if filtro_data_exa_inicio != "" and not datetime.strptime(reg.reg_teste_data_exame, "%Y-%m-%d").date() >= datetime.strptime(filtro_data_exa_inicio, "%Y-%m-%d").date():
                continue
            if filtro_data_exa_fim != "" and not datetime.strptime(reg.reg_teste_data_exame, "%Y-%m-%d").date() <= datetime.strptime(filtro_data_exa_fim, "%Y-%m-%d").date():
                continue
            if filtro_teste_resultado != "" and reg.reg_teste_resultado != filtro_teste_resultado:
                continue
            if filtro_data_add_inicio != "" and not datetime.strptime(reg.reg_data_adicionado, "%Y-%m-%d %H:%M:%S").date() >= datetime.strptime(filtro_data_add_inicio, "%Y-%m-%d").date():
                continue
            if filtro_data_add_fim != "" and not datetime.strptime(reg.reg_data_adicionado, "%Y-%m-%d %H:%M:%S").date() <= datetime.strptime(filtro_data_add_fim, "%Y-%m-%d").date():
                continue
            results.append(reg)
    except:
        return Response(response=json.dumps([]), status=400, mimetype="application/json")
    else:
        return Response(response=json.dumps(results, default=lambda x: x.toDict()), status=200, mimetype="application/json")


@app.route('/api/dados')
def api_dados():
    return json.dumps(utils.get_data())


@app.route('/api/relatorio/<string:fname>')
def api_get_relatorio(fname: str):
    fp = os.path.join("zips/", secure_filename(fname))
    if os.path.isfile(fp):
        return send_file(fp, mimetype="application/zip")
    else:
        return Response(status=404)


@app.route('/api/registrar', methods=["POST"])
def api_registrar():
    try:
        reg = Registro.new(**{f"reg_{dado['nome']}": request.form[f"reg_{dado['nome']}"] for dado in utils.get_data() if dado["coletar"]})
    except KeyError:
        return Response(response=f"Erro ao adicionar registro, dados insuficientes", status=400)
    except Exception:
        return Response(response=f"Erro ao adicionar registro", status=400)
    else:
        return Response(response=f"""Adicionado com sucesso: '{reg.brief()}'""", status=201)


@app.route('/api/gen_relatorio', methods=["POST"])
def api_gen_relatorio():
    fpath = sheet_maker.zip_files(sheet_maker.make_sheet(regs=Registro.get_ids(request.form.getlist("reg_ids"))), remove_dirs=True)
    return url_for("api_get_relatorio", fname=os.path.split(fpath)[1])


@app.route('/api/update', methods=["POST"])
def api_update_registro():
    # post request
    try:
        Registro.update(**request.form)
    except:
        return Response(status=400)
    else:
        return Response(status=200)


@app.route('/api/delete', methods=["POST"])
def api_delete_registro():
    # post request
    try:
        Registro.delete(**request.form)
    except Exception as e:
        print(e)
        return Response(response="Erro ao deletar registro", status=400)
    else:
        return Response(response="Registro deletado com sucesso", status=200)


@app.route('/api/get_data_from_spreadsheet', methods=["POST"])
def api_get_data_from_spreadsheet():
    # post request
    try:
        records = planilha.get_new_records()
        dados = utils.get_data()
    except:
        return Response(response="Erro ao processar planilha", status=400)
    else:
        return Response(response=json.dumps({"dados": dados, "registros": records}, default=lambda x: x.toDict()), status=200)


@app.route('/api/delete_inserted_data_from_spreadsheet', methods=["POST"])
def api_delete_inserted_data_from_spreadsheet():
    # post request
    try:
        planilha.delete_inserted_data()
    except:
        return Response(response="Erro ao deletar dados da planilha", status=400)
    else:
        return Response(response="Dados deletados com sucesso", status=200)


if __name__ == '__main__':
    import platform

    if platform.system() == "Windows":
        app.run(host="0.0.0.0", port=5000, debug=True)
    elif platform.system() == "Linux":
        app.run(host='0.0.0.0', port=8001, debug=False)
