from flask import Flask, render_template, request
from registro import Registro
import json

app = Flask(__name__)


@app.route('/')
def resumo_page():
    return render_template("resumo.html")


@app.route('/adicionar', methods=["GET", "POST"])
def add_register_page():
    if request.method == "POST":
        # post request
        reg_ra = request.form["reg_ra"]
        reg_nome_animal = request.form["reg_nome_animal"]
        reg_endereco_nome_dono = request.form["reg_endereco_nome_dono"]
        reg_quadra = request.form["reg_quadra"]
        reg_situacao_coleta = request.form["reg_situacao_coleta"]
        reg_data_coleta = request.form["reg_data_coleta"]
        reg_teste_data_exame = request.form["reg_teste_data_exame"]
        reg_teste_resultado = request.form["reg_teste_resultado"]
        reg_exame_numero_amostra = request.form["reg_exame_numero_amostra"]
        reg_exame_data = request.form["reg_exame_data"]
        reg_exame_resultado = request.form["reg_exame_resultado"]
        reg_sintomas = request.form["reg_sintomas"]
        reg_eutanasia_realizada = request.form["reg_eutanasia_realizada"]
        reg_eutanasia_data = request.form["reg_eutanasia_data"]

        try:
            reg = Registro.new(
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
                reg_eutanasia_data=reg_eutanasia_data)
        except:
            return render_template("adicionar_registro.html", error_message="Erro ao adicionar registro")
        else:
            return render_template("adicionar_registro.html", success_message=f"""Adicionado com sucesso: {reg.brief()}""")
    else:
        # get request
        return render_template("adicionar_registro.html")


@app.route("/api/get")
def api_get():
    registros = Registro.get_all()
    return json.dumps([reg.__dict__ for reg in registros])


if __name__ == '__main__':
    import platform

    if platform.system() == "Windows":
        app.run(host="0.0.0.0", port=5000, debug=True)
    elif platform.system() == "Linux":
        app.run(host='0.0.0.0', port=80, debug=False)
