function date_from_localtimezone(datetime) {
    let d = new Date(datetime);
    d.setTime(d.getTime() + d.getTimezoneOffset() * 60000);
    if (d instanceof Date && !isNaN(d))
        return d;
    else
        return new Date(0);
}

document.onreadystatechange = function () {
    if (document.readyState === "complete") {
        Promise.all([fetch("/api/dados").then(r => r.json()), fetch("/api/registros?desc").then(r => r.json())])
            .then(function ([dados, registros]) {
                let table = document.getElementById("registros");
                let thead = document.createElement("thead");
                {
                    let tr = document.createElement("tr");
                    for (let i = 0; i < dados.length; i++) {
                        if (dados[i]["mostrar"] === null) continue;
                        let th = document.createElement("th");
                        th.innerText = dados[i]["mostrar"];
                        tr.appendChild(th);
                    }
                    thead.appendChild(tr);
                }

                table.appendChild(thead);
                let tbody = document.createElement("tbody");
                for (let i = 0; i < registros.length; i++) {
                    let tr = document.createElement("tr");
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
                        else if (dados[j]["valores"][registros[i][`reg_${dados[j]["nome"]}`]] !== "")
                            text = dados[j]["valores"][registros[i][`reg_${dados[j]["nome"]}`]];
                        td.innerText = text === "" ? "---" : text;
                        tr.appendChild(td);
                    }
                    tbody.appendChild(tr);
                }
                table.appendChild(tbody);
            });
    }
};
