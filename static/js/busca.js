function date_from_localtimezone(datetime) {
    let d = new Date(datetime);
    d.setTime(d.getTime() + d.getTimezoneOffset() * 60000);
    if (d instanceof Date && !isNaN(d))
        return d;
    else
        return new Date(0);
}


function make_get_params(params) {
    let listparams = [];
    for (let key in params) {
        listparams.push(`${key}=${params[key]}`);
    }
    return listparams.join("&")
}

function edit_registry(id) {
    window.location.href = "/registro?id=" + id;
}


function update_regs() {
    let fd = new FormData(document.getElementById("form_registros_relatorio"));
    let filters_dict = {};
    for (let [key, val] of fd.entries()) filters_dict[key] = val;
    let filters = make_get_params(filters_dict);
    Promise.all([fetch("/api/dados").then(r => r.json()), fetch("/api/registros?desc&" + filters).then(r => r.json())])
        .then(function ([dados, registros]) {
            let table = document.getElementById("registros");
            table.innerHTML = "";
            let thead = document.createElement("thead");
            let trh = document.createElement("tr");

            {
                let th = document.createElement("th");
                th.innerText = "Editar";
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
            for (let i = 0; i < registros.length; i++) {
                let tr = document.createElement("tr");
                {
                    let td = document.createElement("td");
                    let button = document.createElement("button");
                    button.type = "button";
                    button.value = registros[i]["reg_id"];
                    button.innerText = "Editar";
                    button.addEventListener('click', function () {
                        edit_registry(button.value);
                    });
                    td.appendChild(button);
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
                table.appendChild(tr);
            }
        });
}


document.onreadystatechange = function () {
    if (document.readyState === "complete") {
        fetch("/api/dados")
            .then(r => r.json())
            .then(function (dados) {
                for (let dado of dados) {
                    if (dado["valores"] !== null) {
                        let select = document.getElementById(`filtros_${dado["nome"]}`);
                        for (let i = 0; i < dado["valores"].length; i++) {
                            let option = document.createElement("option");
                            option.value = i.toString();
                            option.innerText = dado["valores"][i];
                            select.appendChild(option);
                        }
                    }
                }
            });
        update_regs();
        for (let elt of document.getElementsByClassName("change_update")) {
            elt.addEventListener("change", update_regs);
        }
        for (let elt of document.getElementsByClassName("click_update")) {
            elt.addEventListener("click", update_regs);
        }
    }
};

