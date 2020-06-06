fetch("/api/dados")
    .then(response => response.json())
    .then(function (dados) {
        let form = document.createElement("form");
        form.method = "POST";
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
        let submit = document.createElement("input");
        submit.type = "submit";
        form.appendChild(submit);
        document.getElementById("data-collect").appendChild(form);
    });


