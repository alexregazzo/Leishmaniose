CREATE TABLE IF NOT EXISTS registro
(
    reg_id                   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    reg_ra                   TEXT    NULL,
    reg_nome_animal          TEXT    NULL,
    reg_endereco_nome_dono   TEXT    NULL,
    reg_quadra               TEXT    NULL,
    reg_situacao_coleta      TEXT    NULL,
    reg_data_coleta          TEXT    NULL,
    reg_teste_data_exame     TEXT    NULL,
    reg_teste_resultado      TEXT    NULL,
    reg_exame_numero_amostra TEXT    NULL,
    reg_exame_data           TEXT    NULL,
    reg_exame_resultado      TEXT    NULL,
    reg_sintomas             TEXT    NULL,
    reg_eutanasia_realizada  TEXT    NULL,
    reg_eutanasia_data       TEXT    NULL,
    reg_data_adicionado      TEXT    NOT NULL
);