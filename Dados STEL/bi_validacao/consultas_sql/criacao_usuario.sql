CREATE USER 'bi_validacao'@'%' IDENTIFIED BY 'bi_smul2023';
GRANT ALL PRIVILEGES ON bi_validacao.* TO 'bi_validacao'@'%';
FLUSH PRIVILEGES;