function make_checkbox(registro) {
    let checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.name = "reg_ids";
    checkbox.value = registro["reg_id"];
    checkbox.checked = false;
    return checkbox;
}

function update_regs() {
    let filtro_quadra = document.getElementById("filtro_quadra").value;
    let filtro_data_add_inicio = document.getElementById("filtro_data_add_inicio").value;
    let filtro_data_add_fim = document.getElementById("filtro_data_add_fim").value;
    let filtro_data_col_inicio = document.getElementById("filtro_data_col_inicio").value;
    let filtro_data_col_fim = document.getElementById("filtro_data_col_fim").value;
    let filters = make_get_params({filtro_quadra, filtro_data_add_inicio, filtro_data_add_fim, filtro_data_col_inicio, filtro_data_col_fim});
    Promise.all([fetch("/api/dados").then(r => r.json()), fetch("/api/registros?desc&" + filters).then(r => r.json())])
        .then(function ([dados, registros]) {
            let ptable = document.getElementById("registros");
            let ntable = create_table_registros(dados, registros, ["Seleção", make_checkbox]);
            ptable.replaceWith(ntable);
        });
}

function gen_report() {
    fetch("/api/gerar_relatorio",
        {method: "POST", body: new FormData(document.querySelector("#form_registros_relatorio"))})
        .then(resp => resp.text())
        .then(function (path) {
            download(path, path.split("/").slice(-1)[0]);
        })
}

document.onreadystatechange = function () {
    if (document.readyState === "complete") {
        document.getElementById("filtro_data_add_inicio").valueAsDate = get_week_ago(new Date());
        document.getElementById("filtro_data_add_fim").valueAsDate = new Date();
        update_regs();
        for (let elt of document.getElementsByClassName("change_update")) {
            elt.addEventListener("change", update_regs);
        }
        for (let elt of document.getElementsByClassName("click_update")) {
            elt.addEventListener("click", update_regs);
        }
        document.getElementById("gerar_relatorio").addEventListener("click", gen_report)
    }
};