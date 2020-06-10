function submit() {
    let form = document.getElementById("registrar-form");
    let fd = new FormData(form);

    fetch("/api/registrar", {method: "POST", body: fd})
        .then(function (resp) {
            console.log(arguments);
            let elt_suc = document.getElementById("success_message");
            let elt_err = document.getElementById("error_message");
            elt_suc.innerText = "";
            elt_err.innerText = "";
            let elt;
            if (resp.ok) {
                elt = elt_suc;
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
            elt.innerText = text + " " + new Date().toLocaleString();
        });
}


fetch("/api/dados")
    .then(response => response.json())
    .then(function (dados) {
        let form = document.createElement("form");
        form.id = "registrar-form";
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
        let input_container = document.createElement("div");
        input_container.classList.add("input-container");
        let button = document.createElement("button");
        button.type = "button";
        button.innerText = "Registrar";
        button.addEventListener("click", submit);
        input_container.appendChild(button);
        form.appendChild(input_container);
        document.getElementById("data-collect").appendChild(form);
    });


