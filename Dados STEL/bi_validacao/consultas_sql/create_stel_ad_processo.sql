/*Criação tabela stel_ad_processo*/
USE bi_validacao;
CREATE TABLE stel_ad_processo (
    id VARCHAR(30),
    protocolo VARCHAR(20),
    n_processo VARCHAR(20) NULL,
    data_autuacao VARCHAR(20) NULL,
    assunto VARCHAR(150),
    setor_autuacao VARCHAR(20) NULL,
    setor_atual VARCHAR(20) NULL,
    proc_status VARCHAR(40),
    situacao_atual VARCHAR(255),
    data_situacao_atual VARCHAR(20),
    data_extracao DATE,
    link VARCHAR(150)
    );

    
/*Carga de dados*/
LOAD DATA INFILE 'C:\\Users\\d850398\\Documents\\GitHub\\py_ad_extraction\\arquivos_extracao\\ad_processos_raw.csv'
INTO TABLE stel_ad_processo
FIELDS TERMINATED BY ';' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;  -- Ignorar a primeira linha do CSV

/*Transformação dos dados*/
SET SQL_SAFE_UPDATES = 0;
-- Alterando campos vazios para NULL
UPDATE stel_ad_processo
SET data_autuacao = NULL
WHERE data_autuacao = '';

UPDATE stel_ad_processo
SET n_processo = NULL
WHERE n_processo = '';

UPDATE stel_ad_processo
SET setor_autuacao = NULL
WHERE setor_autuacao = '';

UPDATE stel_ad_processo
SET setor_atual = NULL
WHERE setor_atual = '';


-- modificando campos de data para DATE
	/*data_autuacao*/
ALTER TABLE stel_ad_processo -- data_autuacao
ADD data_autuacao_date DATETIME NULL;
UPDATE stel_ad_processo
SET data_autuacao_date = str_to_date(data_autuacao, '%d/%m/%Y %H:%i:%s')
WHERE data_autuacao IS NOT NULL;
ALTER TABLE stel_ad_processo
DROP COLUMN data_autuacao;
ALTER TABLE stel_ad_processo
CHANGE data_autuacao_date data_autuacao DATETIME NULL;

	/*data_situacao_atual*/
ALTER TABLE stel_ad_processo
ADD data_situacao_atual_date DATETIME NULL;
UPDATE stel_ad_processo
SET data_situacao_atual_date = str_to_date(data_situacao_atual, '%d/%m/%Y %H:%i:%s')
WHERE data_situacao_atual IS NOT NULL;
ALTER TABLE stel_ad_processo
DROP COLUMN data_situacao_atual;
ALTER TABLE stel_ad_processo
CHANGE data_situacao_atual_date data_situacao_atual DATETIME NULL;

/*Dropando colunas sem uso*/
ALTER TABLE stel_ad_processo
DROP COLUMN id;
ALTER TABLE stel_ad_processo
DROP COLUMN setor_autuacao;
ALTER TABLE stel_ad_processo
DROP COLUMN setor_atual;
ALTER TABLE stel_ad_processo
DROP COLUMN situacao_atual;
ALTER TABLE stel_ad_processo
DROP COLUMN link;
ALTER TABLE stel_ad_processo
DROP COLUMN data_situacao_atual;
SET SQL_SAFE_UPDATES = 1;


/*Show Data*/
SELECT *
FROM bi_validacao.stel_ad_processo;

/*restart*/
DROP TABLE stel_ad_processo;


SELECT COLUMN_NAME, COLLATION_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'stel_ad_processo'
