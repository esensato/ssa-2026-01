CREATE TABLE modelos (
    modelo_id INT PRIMARY KEY,
    marca_id INT,
    nome_modelo VARCHAR(100)
);

CREATE TABLE vendas (
    registro_id INT PRIMARY KEY,
    marca_id INT,
    modelo_id INT,
    ano_modelo VARCHAR(10),
    data_venda DATE,
    valor_venda DECIMAL(10,2),
    taxa_servico DECIMAL(10,2),
    valor_total DECIMAL(10,2),
    km_rodados INT,
    placa VARCHAR(10),
    cliente VARCHAR(100),
    estado VARCHAR(5)
);

CREATE TABLE fipe_valores (
    marca_id INT,
    modelo_id INT,
    ano_modelo VARCHAR(10),
    valor_fipe DECIMAL(10,2)
);

INSERT INTO modelos VALUES (5940,59,'VW Golf');
INSERT INTO modelos VALUES (4828,21,'Fiat Uno');
INSERT INTO modelos VALUES (6831,23,'Ford Ka');
INSERT INTO modelos VALUES (9120,22,'Chevrolet Onix');
INSERT INTO modelos VALUES (7710,44,'Toyota Corolla');

INSERT INTO fipe_valores VALUES (59,5940,'2014-1',88629.00);
INSERT INTO fipe_valores VALUES (59,5940,'2015-1',91000.00);

INSERT INTO fipe_valores VALUES (21,4828,'2018-2',45990.00);
INSERT INTO fipe_valores VALUES (21,4828,'2019-1',48000.00);

INSERT INTO fipe_valores VALUES (23,6831,'2020-1',73500.00);
INSERT INTO fipe_valores VALUES (23,6831,'2021-1',76000.00);

INSERT INTO fipe_valores VALUES (22,9120,'2019-3',52300.00);
INSERT INTO fipe_valores VALUES (22,9120,'2020-2',54800.00);

INSERT INTO fipe_valores VALUES (44,7710,'2017-1',39900.00);
INSERT INTO fipe_valores VALUES (44,7710,'2018-1',42000.00);

INSERT INTO vendas VALUES
(1,59,5940,'2014-1','2025-01-10',88629.00,1200,89829,120000,'ABC1D23','Joao Silva','SP'),
(2,59,5940,'2014-1','2025-01-12',88629.00,1200,89829,118000,'ABC1D24','Maria Souza','SP'),
(3,59,5940,'2015-1','2025-01-15',91200.00,1200,92400,98000,'ABC1D25','Carlos Pereira','RJ'),

(4,21,4828,'2018-2','2025-01-18',45990.00,900,46890,87000,'DEF4K56','Ana Lima','MG'),
(5,21,4828,'2018-2','2025-01-20',45990.00,900,46890,86000,'DEF4K57','Paulo Mendes','MG'),

(6,21,4828,'2019-1','2025-01-25',48900.00,900,49800,76000,'DEF4K58','Lucas Prado','SP'),

(7,23,6831,'2020-1','2025-02-01',73500.00,1000,74500,65000,'GHI7L89','Juliana Costa','PR'),
(8,23,6831,'2020-1','2025-02-03',73500.00,1000,74500,64000,'GHI7L90','Ricardo Alves','PR'),
(9,23,6831,'2021-1','2025-02-05',75500.00,1000,76500,52000,'GHI7L91','Fernanda Rocha','SC'),

(10,22,9120,'2019-3','2025-02-10',52300.00,850,53150,42000,'JKL2P45','Andre Martins','RS'),
(11,22,9120,'2019-3','2025-02-12',52300.00,850,53150,41000,'JKL2P46','Patricia Nunes','RS'),

(12,22,9120,'2020-2','2025-02-15',54800.00,850,55650,35000,'JKL2P47','Marcos Dias','SP'),

(13,44,7710,'2017-1','2025-02-18',39900.00,700,40600,87000,'MNO9T12','Renata Farias','RJ'),
(14,44,7710,'2017-1','2025-02-20',39900.00,700,40600,86000,'MNO9T13','Bruna Carvalho','RJ'),
(15,44,7710,'2018-1','2025-02-22',42000.00,700,42700,80000,'MNO9T14','Julio Castro','SP'),

-- problema de integridade (modelo inexistente)
(16,21,9999,'2018-2','2025-03-01',45990.00,900,46890,90000,'PQR5S67','Lucas Teixeira','SP'),

-- problema de acurácia (valor muito acima da FIPE)
(17,59,5940,'2014-1','2025-03-02',120000.00,1200,121200,121000,'PQR5S68','Paula Teixeira','SP'),

-- problema de acurácia (valor muito abaixo)
(18,23,6831,'2020-1','2025-03-04',50000.00,1000,51000,100000,'PQR5S69','Juliana Costa','RJ');

