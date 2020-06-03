let column_names = ["reg_ra",
    "reg_nome_animal",
    "reg_endereco_nome_dono",
    "reg_quadra",
    "reg_situacao_coleta",
    "reg_data_coleta",
    "reg_teste_data_exame",
    "reg_teste_resultado",
    "reg_exame_numero_amostra",
    "reg_exame_data",
    "reg_exame_resultado",
    "reg_sintomas",
    "reg_eutanasia_realizada",
    "reg_eutanasia_data",
    "reg_data_adicionado"];
let quadra = null;

function get_registros() {
    fetch("/api/get")
        .then(response => response.json())
        .then(function (registros) {
            let html = "<tr>\n" +
                "        <th>RA</th>\n" +
                "        <th>Nome animal</th>\n" +
                "        <th>Endereço / Nome dono</th>\n" +
                "        <th>Quadra</th>\n" +
                "        <th>Situação coleta</th>\n" +
                "        <th>Data coleta</th>\n" +
                "        <th>Teste: data exame</th>\n" +
                "        <th>Teste: resultado exame</th>\n" +
                "        <th>Exame: Numero amostra</th>\n" +
                "        <th>Exame: data</th>\n" +
                "        <th>Exame: Resultado</th>\n" +
                "        <th>Sintomas</th>\n" +
                "        <th>Eutanasia realizada</th>\n" +
                "        <th>Eutanasia data</th>\n" +
                "        <th>Registrado em</th>\n" +
                "    </tr>";
            for (let reg of registros) {
                if (quadra !== null && reg["reg_quadra"] !== quadra) continue;
                html += "<tr>";
                for (let cname of column_names) {
                    html += `<td>${reg[cname]}</td>`;
                }
                html += "</tr>";
            }
            document.getElementById("registros").innerHTML = html;
        });

}


/*
reg_ra
reg_nome_animal
reg_endereco_nome_dono
reg_quadra
reg_situacao_coleta
reg_data_coleta
reg_teste_data_exame
reg_teste_resultado
reg_exame_numero_amostra
reg_exame_data
reg_exame_resultado
reg_sintomas
reg_eutanasia_realizada
reg_eutanasia_data
reg_data_adicionado

* 
*/

get_registros();

function update_quadra_filter(elt) {
    if (elt.value < 0) {
        quadra = null;
    } else {
        quadra = elt.value.toString();
    }
    get_registros();
}


// setTimeout("window.location.reload()", 2000);