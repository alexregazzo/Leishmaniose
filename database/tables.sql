CREATE TABLE IF NOT EXISTS registro
(
    reg_id               INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    reg_ra               TEXT    NOT NULL,
    reg_nome_animal      TEXT    NOT NULL,
    reg_nome_dono        TEXT    NOT NULL,
    reg_endereco         TEXT    NOT NULL,
    reg_quadra           TEXT    NOT NULL,
    reg_situacao_coleta  TEXT    NOT NULL,
    reg_data_coleta      TEXT    NOT NULL,
    reg_teste_data_exame TEXT    NOT NULL,
    reg_teste_resultado  TEXT    NOT NULL,
    reg_data_adicionado  TEXT    NOT NULL
);