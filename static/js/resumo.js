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
                let trh = document.createElement("tr");
                for (let i = 0; i < dados.length; i++) {
                    if (dados[i]["mostrar"] === null) continue;
                    let th = document.createElement("th");
                    th.innerText = dados[i]["mostrar"];
                    trh.appendChild(th);
                }
                table.appendChild(trh);
                for (let i = 0; i < registros.length; i++) {
                    let tr = document.createElement("tr");
                    for (let j = 0; j < dados.length; j++) {
                        if (dados[j]["mostrar"] === null) continue;
                        let td = document.createElement("td");
                        if (dados[j]["tipo"] === "date")
                            td.innerText = date_from_localtimezone(registros[i][`reg_${dados[j]["nome"]}`]).toLocaleDateString();
                        else if (dados[j]["tipo"] === "datetime")
                            td.innerText = date_from_localtimezone(registros[i][`reg_${dados[j]["nome"]}`]).toLocaleString();
                        else if (dados[j]["valores"] === null)
                            td.innerText = registros[i][`reg_${dados[j]["nome"]}`];
                        else
                            td.innerText = dados[j]["valores"][registros[i][`reg_${dados[j]["nome"]}`]];
                        tr.appendChild(td);
                    }
                    table.appendChild(tr);
                }
            });
    }
};
