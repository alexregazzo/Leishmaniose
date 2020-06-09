function make_edit(registro) {
    let button = document.createElement("button");
    button.type = "button";
    button.value = registro["reg_id"];
    button.innerText = "Editar";
    button.addEventListener('click', function () {
        edit_registry(button.value);
    });
    return button;
}


function edit_registry(id) {
    window.location.href = "/registro?id=" + id;
}


function update_regs() {
    let fd = new FormData(document.getElementById("form_registros_relatorio"));
    let filters_dict = {};
    for (let [key, val] of fd.entries()) filters_dict[key] = val;
    let filters = make_get_params(filters_dict);
    console.log(filters);
    Promise.all([fetch("/api/dados").then(r => r.json()), fetch("/api/registros?desc&" + filters).then(r => r.json())])
        .then(function ([dados, registros]) {
            let ptable = document.getElementById("registros");
            let ntable = create_table_registros(dados, registros, ["Editar", make_edit]);
            ptable.replaceWith(ntable);
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
                            if (dado["valores"][i] !== "") option.value = i.toString();
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

