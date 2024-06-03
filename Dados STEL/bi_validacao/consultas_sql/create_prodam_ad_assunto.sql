
/*restart*/
DROP TABLE prodam_ad_assunto;
/*Criação tabela prodam_ad_assunto*/
USE bi_validacao;
CREATE TABLE prodam_ad_assunto (
	sistema				varchar(50)   NULL,
	processo			varchar(50)   NULL,
	protocolo			varchar(50)   NULL,
	codigoAssuntoObra   varchar(50)   NULL,   
	ano					varchar(50)   NULL,
	dtInclusaoAssunto	date          NULL,
	assuntoCod			varchar(50)    NULL,
	assunto			   	varchar(400)  NULL,
	situacaoAssunto    	varchar(50)   NULL,
	numeroAlvara		varchar(50)   NULL,
	dtEmissaoAlvara		varchar(50)   NULL,
	statusAlvara		varchar(50)   NULL,
	codigoProcesso 		varchar(50)	  NULL,
	digitoProcesso		varchar(50)	  NULL
    );
    
/*Carga de dados*/
LOAD DATA INFILE 'C:\\Users\\d850398\\Documents\\GitHub\\dados_COTIS\\bi_validacao\\tabelas_prodam\\prodam_ad_assunto.csv'
INTO TABLE prodam_ad_assunto
CHARACTER SET latin1
FIELDS TERMINATED BY ';' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;  -- Ignorar a primeira linha do CSV

SET SQL_SAFE_UPDATES = 0;
UPDATE prodam_ad_assunto
SET assunto = REPLACE(assunto, 'Ã¡', 'á')
WHERE assunto LIKE '%Ã¡%';

UPDATE prodam_ad_assunto
SET situacaoAssunto = REPLACE(assunto, 'Ã¡', 'á')
WHERE situacaoAssunto LIKE '%Ã¡%';

UPDATE prodam_ad_assunto
SET assunto = REPLACE(assunto, 'Ã§', 'ç')
WHERE assunto LIKE '%Ã§%';

UPDATE prodam_ad_assunto
SET assunto = REPLACE(assunto, 'Ã£', 'ã')
WHERE assunto LIKE '%Ã£%';

UPDATE prodam_ad_processo
SET processo = NULL
WHERE processo = '';

UPDATE prodam_ad_processo
SET assuntoCod = NULL
WHERE assuntoCod = 'NULL';

UPDATE prodam_ad_processo
SET numeroAlvara = NULL
WHERE numeroAlvara = 'NULL';

UPDATE prodam_ad_processo
SET statusAlvara = NULL
WHERE statusAlvara = 'NULL';

UPDATE prodam_ad_processo
SET digitoProcesso = NULL
WHERE digitoProcesso = 'NULL';


SET SQL_SAFE_UPDATES = 1;


/*Show Data*/
SELECT *
FROM bi_validacao.prodam_ad_assunto;

/*restart*/
DROP TABLE prodam_ad_assunto;


/* group by*/
SELECT situacaoAssunto, COUNT(*) AS contagem
FROM bi_validacao.prodam_ad_assunto
GROUP BY situacaoAssunto;

SELECT assunto, COUNT(*) AS contagem
FROM bi_validacao.prodam_ad_assunto
GROUP BY assunto;


SELECT COLUMN_NAME, COLLATION_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'prodam_ad_processo';

SELECT assunto, COUNT(*) AS contagem
FROM bi_validacao.prodam_ad_processo
GROUP BY situacao
