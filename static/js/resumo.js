document.onreadystatechange = function () {
    if (document.readyState === "complete") {
        Promise.all([fetch("/api/dados").then(r => r.json()), fetch("/api/registros?desc").then(r => r.json())])
            .then(function ([dados, registros]) {
                let ptable = document.getElementById("registros");
                let ntable = create_table_registros(dados, registros);
                ptable.replaceWith(ntable);
            });
    }
};
