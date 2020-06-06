from flask import Flask, render_template, request, Response, send_file, url_for
from werkzeug.utils import secure_filename
import os
from registro import Registro
import utils
import json
from datetime import datetime
import sheet_maker

app = Flask(__name__)


@app.route('/')
def resumo_page():
    return render_template("resumo.html")


@app.route("/gerar_relatorio")
def gerar_relatorio_page():
    return render_template("gen_relatorio.html")


@app.route('/adicionar', methods=["GET", "POST"])
def add_register_page():
    if request.method == "POST":
        # post request
        coletados = {}
        for dado in utils.get_data():
            if dado["coletar"]:
                try:
                    coletados[f"reg_{dado['nome']}"] = request.form[f"reg_{dado['nome']}"]
                except KeyError as e:
                    return render_template("adicionar.html", error_message=f"Erro ao adicionar registro, dados insuficientes, faltando: '{str(e)}'")
        try:
            reg = Registro.new(**coletados)
        except:
            return render_template("adicionar.html", error_message="Erro ao adicionar registro")
        else:
            return render_template("adicionar.html", success_message=f"""Adicionado com sucesso: {reg.brief()}""")
    else:
        # get request
        return render_template("adicionar.html")


@app.route("/api/registros")
def api_get():
    filtro_quadra = request.args.get("filtro_quadra", "")
    filtro_data_add_inicio = request.args.get("filtro_data_add_inicio", "")
    filtro_data_add_fim = request.args.get("filtro_data_add_fim", "")
    filtro_data_col_inicio = request.args.get("filtro_data_col_inicio", "")
    filtro_data_col_fim = request.args.get("filtro_data_col_fim", "")

    regs = Registro.get_all(desc=request.args.get("desc", None) is not None)
    results = []
    try:
        for reg in regs:
            if filtro_quadra != "" and reg["reg_quadra"] != filtro_quadra:
                continue
            if filtro_data_add_inicio != "" and not datetime.strptime(reg.reg_data_adicionado, "%Y-%m-%d %H:%M:%S").date() >= datetime.strptime(filtro_data_add_inicio, "%Y-%m-%d").date():
                continue
            if filtro_data_add_fim != "" and not datetime.strptime(reg.reg_data_adicionado, "%Y-%m-%d %H:%M:%S").date() <= datetime.strptime(filtro_data_add_fim, "%Y-%m-%d").date():
                continue
            if filtro_data_col_inicio != "" and not datetime.strptime(reg.reg_data_coleta, "%Y-%m-%d").date() >= datetime.strptime(filtro_data_col_inicio, "%Y-%m-%d").date():
                continue
            if filtro_data_col_fim != "" and not datetime.strptime(reg.reg_data_coleta, "%Y-%m-%d").date() <= datetime.strptime(filtro_data_col_fim, "%Y-%m-%d").date():
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
    print(fp)
    if os.path.isfile(fp):
        return send_file(fp, mimetype="application/zip")
    else:
        return Response(status=404)


@app.route('/api/gen_relatorio', methods=["POST"])
def api_gen_relatorio():
    fpath = sheet_maker.zip_files(sheet_maker.make_sheet(regs=Registro.get_ids(request.form.getlist("reg_ids"))), remove_dirs=True)
    return url_for("api_get_relatorio", fname=os.path.split(fpath)[1])


if __name__ == '__main__':
    import platform

    if platform.system() == "Windows":
        app.run(host="0.0.0.0", port=5000, debug=True)
    elif platform.system() == "Linux":
        app.run(host='0.0.0.0', port=8001, debug=False)
