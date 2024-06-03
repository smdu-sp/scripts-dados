LOAD DATA INFILE 'C:\Users\d850398\Documents\GitHub\py_ad_extraction\arquivos_extracao\ad_processos_raw.csv'
INTO TABLE ad_processo
FIELDS TERMINATED BY ';' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;  -- Ignorar a primeira linha do CSV