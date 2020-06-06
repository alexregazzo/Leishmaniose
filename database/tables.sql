CREATE TABLE IF NOT EXISTS registro
(
    reg_id                   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    reg_ra                   TEXT    NULL,
    reg_nome_animal          TEXT    NULL,
    reg_quadra               TEXT    NULL,
    reg_situacao_coleta      TEXT    NULL,
    reg_data_coleta          TEXT    NULL,
    reg_teste_data_exame     TEXT    NULL,
    reg_teste_resultado      TEXT    NULL,
    reg_data_adicionado      TEXT    NOT NULL
);