function date_from_localtimezone(datetime) {
    let d = new Date(datetime);
    d.setTime(d.getTime() + d.getTimezoneOffset() * 60000);
    if (d instanceof Date && !isNaN(d))
        return d;
    else
        return new Date(0);
}

function download(dataurl, filename) {
    let a = document.createElement("a");
    a.href = dataurl;
    a.setAttribute("download", filename);
    a.click();
}


function make_get_params(params) {
    let listparams = [];
    for (let key in params) {
        listparams.push(`${key}=${params[key]}`);
    }
    return listparams.join("&")
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
            let table = document.getElementById("registros");
            table.innerHTML = "";
            let thead = document.createElement("thead");
            let trh = document.createElement("tr");
            {
                let th = document.createElement("th");
                th.innerText = "Seleção";
                trh.appendChild(th);
            }
            for (let i = 0; i < dados.length; i++) {
                if (dados[i]["mostrar"] === null) continue;
                let th = document.createElement("th");
                th.innerText = dados[i]["mostrar"];
                trh.appendChild(th);
            }
            thead.appendChild(trh);
            table.appendChild(thead);
            let tbody = document.createElement("tbody");
            for (let i = 0; i < registros.length; i++) {
                let tr = document.createElement("tr");
                {
                    let td = document.createElement("td");
                    let checkbox = document.createElement("input");
                    checkbox.type = "checkbox";
                    checkbox.name = "reg_ids";
                    checkbox.value = registros[i]["reg_id"];
                    checkbox.checked = true;
                    td.appendChild(checkbox);
                    tr.appendChild(td);
                }

                for (let j = 0; j < dados.length; j++) {
                    if (dados[j]["mostrar"] === null) continue;
                    let td = document.createElement("td");
                    let text = "";
                    if (dados[j]["tipo"] === "date")
                        text = date_from_localtimezone(registros[i][`reg_${dados[j]["nome"]}`]).toLocaleDateString();
                    else if (dados[j]["tipo"] === "datetime")
                        text = date_from_localtimezone(registros[i][`reg_${dados[j]["nome"]}`]).toLocaleString();
                    else if (dados[j]["valores"] === null)
                        text = registros[i][`reg_${dados[j]["nome"]}`];
                    else
                        text = dados[j]["valores"][registros[i][`reg_${dados[j]["nome"]}`]];
                    td.innerText = text === "" ? "---" : text;
                    tr.appendChild(td);
                }
                tbody.appendChild(tr);
            }
            table.appendChild(tbody);
        });
}

function gen_report() {
    fetch("/api/gen_relatorio",
        {method: "POST", body: new FormData(document.querySelector("#form_registros_relatorio"))})
        .then(resp => resp.text())
        .then(function (path) {
            download(path, path.split("/").slice(-1)[0]);
        })
}

document.onreadystatechange = function () {
    if (document.readyState === "complete") {
        document.getElementById("filtro_data_add_inicio").valueAsDate = new Date();
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