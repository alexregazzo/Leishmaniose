function date_from_localtimezone(datetime) {
    let d = new Date(datetime);
    d.setTime(d.getTime() + d.getTimezoneOffset() * 60000);
    if (d instanceof Date && !isNaN(d))
        return d;
    else
        return new Date(0);
}

function parse_data(dado, texto) {
    // return texto;
    if (texto === "") {
        return "---"
    } else if (dado["tipo"] === "date") {
        return date_from_localtimezone(texto).toLocaleDateString();
    } else if (dado["tipo"] === "datetime") {
        return date_from_localtimezone(texto).toLocaleString();
    } else if (dado["valores"] !== null) {
        return dado["valores"][texto] === "" ? "---" : dado["valores"][texto];
    } else {
        return texto;
    }
}


function create_table_registros(dados, registros, add_before_every_column = null, add_after_every_column = null) {
    // adds before and after should be like:
    /*
    * ["name", function]
    *  Will be called as
    * column header = "name"
    * column row = function(registro, i) should return TEXT added as HTML to tag
    * */

    let table = document.createElement("table");
    table.id = "registros";
    let thead = document.createElement("thead");
    {
        let tr = document.createElement("tr");
        if (add_before_every_column !== null) {
            let th = document.createElement("th");
            th.innerHTML = add_before_every_column[0];
            tr.appendChild(th);
        }
        for (let i = 0; i < dados.length; i++) {
            if (dados[i]["mostrar"] === null) continue;
            let th = document.createElement("th");
            th.innerText = dados[i]["mostrar"];
            tr.appendChild(th);
        }
        if (add_after_every_column !== null) {
            let th = document.createElement("th");
            th.innerHTML = add_after_every_column[0];
            tr.appendChild(th);
        }
        thead.appendChild(tr);
    }

    table.appendChild(thead);
    let tbody = document.createElement("tbody");
    for (let i = 0; i < registros.length; i++) {
        let tr = document.createElement("tr");
        if (add_before_every_column !== null) {
            let td = document.createElement("td");
            let elt = add_before_every_column[1](registros[i], i);
            if (typeof elt === "object") {
                td.appendChild(elt);
            } else {
                td.innerHTML = elt;
            }
            tr.appendChild(td);
        }
        for (let j = 0; j < dados.length; j++) {
            if (dados[j]["mostrar"] === null) continue;
            let td = document.createElement("td");

            td.innerText = parse_data(dados[j], registros[i][`reg_${dados[j]["nome"]}`]);
            tr.appendChild(td);
        }
        if (add_after_every_column !== null) {
            let td = document.createElement("td");
            let elt = add_after_every_column[1](registros[i], i);
            if (typeof elt === "object") {
                td.appendChild(elt);
            } else {
                td.innerHTML = elt;
            }
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    }
    table.appendChild(tbody);
    return table;
}

function make_get_params(params) {
    let listparams = [];
    for (let key in params) {
        listparams.push(`${key}=${params[key]}`);
    }
    return listparams.join("&")
}

function download(dataurl, filename) {
    let a = document.createElement("a");
    a.href = dataurl;
    a.setAttribute("download", filename);
    a.click();
}

function get_week_ago(d) {
    return new Date(d.getTime() - d.getTime() % (24 * 60 * 60 * 1000) + d.getTimezoneOffset() * 60000 - 7 * 24 * 60 * 60 * 1000);
}
