function make_date_from_locale(datestr) {
    return new Date(datestr.split("/").reverse().join("/"));
}

function get_registry() {
    let urlParams = new URLSearchParams(window.location.search);
    let id = urlParams.get("id");
    Promise.all([fetch("/api/dados").then(r => r.json()), fetch(`/api/registros?filtro_id=${id}`).then(r => r.json())])
        .then(function ([dados, registros]) {
            if (registros.length !== 1) {
                document.getElementById("error_message").innerText = "Erro ao encontrar o registro";
                return;
            }
            let registro = registros[0];
            let form = document.createElement("form");
            form.id = "form-registro";
            {
                let reg_id = document.createElement("input");
                reg_id.name = "reg_id";
                reg_id.hidden = true;
                reg_id.value = id;
                form.appendChild(reg_id);
            }

            for (let dado of dados) {
                if (dado["coletar"] === null) continue;
                let div = document.createElement("div");
                div.classList.add("input-container");
                let label = document.createElement("label");
                label.innerText = `${dado['mostrar']}: `;
                div.appendChild(label);
                if (dado["valores"] === null) {
                    // no predefined values
                    let input = document.createElement("input");
                    input.type = dado["coletar"];
                    input.name = `reg_${dado['nome']}`;
                    input.required = true;
                    if (dado["coletar"] === "date") {
                        input.valueAsDate = make_date_from_locale(registro[`reg_${dado['nome']}`]);
                    } else {
                        input.value = registro[`reg_${dado['nome']}`];
                    }
                    /*
                    <div class="input-container">
                        <label>Quadra: </label>
                        <input type="number" name="reg_quadra" placeholder="5" required>
                    </div>
                    */
                    div.appendChild(input)
                } else {
                    // with predefined values
                    let select = document.createElement("select");
                    select.name = `reg_${dado['nome']}`;
                    for (let i = 0; i < dado["valores"].length; i++) {
                        let option = document.createElement("option");
                        option.value = i.toString();
                        option.innerText = dado["valores"][i];
                        select.appendChild(option);
                    }
                    select.value = registro[`reg_${dado['nome']}`];
                    select.addEventListener("change", something_changed);
                    /*
                     <div class="input-container">
                        <label>Situação da Coleta: </label>
                        <select name="reg_situacao_coleta">
                        <option value="COLETADO">COLETADO</option>
                     */

                    div.appendChild(select)
                }
                form.appendChild(div);
            }
            let input_container_update = document.createElement("div");
            input_container_update.classList.add("input-container");
            let update_button = document.createElement("button");
            update_button.type = "button";
            update_button.innerText = "Atualizar";
            update_button.addEventListener("click", update_registry);
            input_container_update.appendChild(update_button);
            form.appendChild(input_container_update);
            let input_container_delete = document.createElement("div");
            input_container_delete.classList.add("input-container");
            let delete_button = document.createElement("button");
            delete_button.classList.add("caution");
            delete_button.type = "button";
            delete_button.innerText = "Deletar";
            delete_button.addEventListener("click", delete_registry);
            input_container_delete.appendChild(delete_button);
            form.appendChild(input_container_delete);
            document.getElementById("data-collect").appendChild(form);
        });
}

function update_registry() {
    let fd = new FormData(document.getElementById("form-registro"));
    fetch("/api/update", {method: "POST", body: fd})
        .then(function (resp) {
            let elt_suc = document.getElementById("success_message");
            let elt_err = document.getElementById("error_message");
            elt_suc.innerText = "";
            elt_err.innerText = "";
            if (resp.ok) {
                CHANGED = false;
                elt_suc.innerText = "Atualizado com sucesso " + new Date().toLocaleString();
                document.body.classList.remove("success-animate");
                void document.body.offsetWidth;
                document.body.classList.add("success-animate");
            } else {
                elt_err.innerText = "Erro ao atualizar " + new Date().toLocaleString();
                document.body.classList.remove("error-animate");
                void document.body.offsetWidth;
                document.body.classList.add("error-animate");
            }

        })
}

function delete_registry() {
    let fd = new FormData(document.getElementById("form-registro"));
    if (confirm("Tem certeza que deseja deletar registro?")) {
        fetch("/api/delete", {method: "POST", body: fd})
            .then(function (resp) {
                let elt;
                let elt_suc = document.getElementById("success_message");
                let elt_err = document.getElementById("error_message");
                elt_suc.innerText = "";
                elt_err.innerText = "";
                if (resp.ok) {
                    elt = elt_suc;
                    CHANGED = false;
                    document.body.classList.remove("success-animate");
                    void document.body.offsetWidth;
                    document.body.classList.add("success-animate");
                } else {
                    elt = elt_err;
                    document.body.classList.remove("error-animate");
                    void document.body.offsetWidth;
                    document.body.classList.add("error-animate");
                }
                return Promise.all([elt, resp.text()]);
            })
            .then(function ([elt, text]) {
                elt.innerHTML = text + " " + new Date().toLocaleString();
            })
    }
}

let CHANGED = false;

function something_changed() {
    CHANGED = true;
}

window.addEventListener("beforeunload", function (evt) {
    if (CHANGED) {
        evt.preventDefault();
    }
});


document.onreadystatechange = function () {
    if (document.readyState === "complete") {
        get_registry();
    }
};