function get_data_from_spreadsheet() {
    fetch("/api/get_data_from_spreadsheet", {method: "POST"})
        .then(function (resp) {
            let success_elt = document.getElementById("success-message");
            let error_elt = document.getElementById("error-message");
            success_elt.innerText = "";
            error_elt.innerText = "";
            if (resp.ok) {
                success_elt.innerText = "Processado com sucesso " + new Date().toLocaleString();
                return resp.json();
            } else {
                error_elt.innerText = "Um erro ocorreu ao processar " + new Date().toLocaleString();
            }
        }).then(function (data) {
            let {dados, registros} = data;
            let table = create_table_registros(dados, registros);
            let div = document.getElementById("dados-adicionados");
            div.innerHTML = "";
            div.appendChild(table);
            console.log(dados, registros)
        }
    );
}

function delete_inserted_data_from_spreadsheet() {
    fetch("/api/delete_inserted_data_from_spreadsheet", {method: "POST"})
        .then(function (resp) {
            let success_elt = document.getElementById("success-message");
            let error_elt = document.getElementById("error-message");
            success_elt.innerText = "";
            error_elt.innerText = "";
            if (resp.ok) {
                success_elt.innerText = "Deletado com sucesso " + new Date().toLocaleString();
            } else {
                error_elt.innerText = "Um erro ocorreu ao deletar " + new Date().toLocaleString();
            }
        });
}


document.onreadystatechange = function () {
    if (document.readyState === "complete") {
        document.getElementById("get-data-from-spreadsheet").addEventListener("click", function () {
            get_data_from_spreadsheet();
        });
        document.getElementById("delete-inserted-data-from-spreadsheet").addEventListener("click", function () {
            delete_inserted_data_from_spreadsheet();
        });
    }
};