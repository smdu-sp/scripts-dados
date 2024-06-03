/*Criação tabela prodam_ad_processo*/
USE bi_validacao;
CREATE TABLE prodam_ad_processo (
    sistema VARCHAR(20),
    processo VARCHAR(20) NULL,
    protocolo VARCHAR(20) NULL,
    ano INT NULL,
    dtAberturaProcesso DATE NULL,
    situacao VARCHAR(50) NULL COLLATE latin1_general_ci,
    codigoProcesso VARCHAR(20),
    digitoProcesso VARCHAR(20),
    dt_inclusao DATETIME
    );

    
/*Carga de dados*/
LOAD DATA INFILE 'C:\\Users\\d850398\\Documents\\GitHub\\dados_COTIS\\bi_validacao\\tabelas_prodam\\prodam_ad_processo.csv'
INTO TABLE prodam_ad_processo
CHARACTER SET latin1
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;  -- Ignorar a primeira linha do CSV

SET SQL_SAFE_UPDATES = 0;
UPDATE prodam_ad_processo
SET situacao = REPLACE(situacao, 'Ã¡', 'á')
WHERE situacao LIKE '%Ã¡%';

UPDATE prodam_ad_processo
SET processo = NULL
WHERE processo = '';

UPDATE prodam_ad_processo
SET situacao = NULL
WHERE situacao = '';

UPDATE prodam_ad_processo
SET codigoProcesso = NULL
WHERE codigoProcesso = '';

UPDATE prodam_ad_processo
SET digitoProcesso = NULL
WHERE codigoProcesso = 'NULL';

SET SQL_SAFE_UPDATES = 1;

/*Show Data*/
SELECT *
FROM bi_validacao.prodam_ad_processo
WHERE processo IS NOT NULL;



/*restart*/
DROP TABLE prodam_ad_processo;

SELECT COLUMN_NAME, COLLATION_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'prodam_ad_processo';

/*todas as situações*/
SELECT situacao, COUNT(*) AS contagem
FROM bi_validacao.prodam_ad_processo
GROUP BY situacao;
