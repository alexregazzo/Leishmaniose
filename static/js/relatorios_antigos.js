fetch("/api/relatorios_antigos").then(r => r.json()).then(function (paths) {
    let relatorios = document.getElementById("relatorios");
    for (let path of paths) {
        let filename = path.split("/").slice(-1)[0];
        let a = document.createElement("a");
        a.classList.add("relatorio-link");
        a.innerText = filename;
        a.setAttribute("href", path);
        a.setAttribute("download", filename);
        relatorios.appendChild(a);
    }
});