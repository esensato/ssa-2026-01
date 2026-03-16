CREATE TABLE modelos (
    modelo_id INT PRIMARY KEY NOT NULL,
    marca_id INT,
    nome_modelo VARCHAR(100)
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


