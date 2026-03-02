# ssa-2026-01
Self Service Analytics
### Ambiente Codespages
- Acessar [Codespaces](https://github.com/features/codespaces?locale=pt-BR)
### Dockerfile PostgreSQL
```dockerfile
FROM postgres:15

ENV POSTGRES_DB=imobiliaria
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin123

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
```
- Arquivo sql para caga de dados (`init.sql`)
```SQL
CREATE TABLE proprietarios (
    cpf VARCHAR(14) PRIMARY KEY,
    nome VARCHAR(100),
    cidade VARCHAR(100)
);

INSERT INTO proprietarios (cpf, nome, cidade) VALUES
('111.111.111-11', 'Carlos Silva', 'São Paulo'),
('222.222.222-22', 'Ana Souza', 'Rio de Janeiro'),
('333.333.333-33', 'Mariana Lima', 'Belo Horizonte'),
('444.444.444-44', 'João Pereira', 'Curitiba'),
('555.555.555-55', 'Fernanda Alves', 'Porto Alegre'),
('666.666.666-66', 'Ricardo Mendes', 'Salvador'),
('777.777.777-77', 'Juliana Rocha', 'Fortaleza'),
('888.888.888-88', 'Eduardo Martins', 'Recife'),
('999.999.999-99', 'Camila Barros', 'Brasília'),
('101.101.101-10', 'Lucas Nogueira', 'Manaus'),
('202.202.202-20', 'Patricia Gomes', 'Florianópolis'),
('303.303.303-30', 'André Carvalho', 'Vitória'),
('404.404.404-40', 'Bianca Ribeiro', 'Goiânia'),
('505.505.505-50', 'Thiago Costa', 'Natal'),
('606.606.606-60', 'Larissa Freitas', 'Belém');
```
- Montagem e execução do container
```bash
docker build -t bd-postgres .
docker run -d -p 5432:5432 --name bd-postgres bd-postgres
```
### Dockerfile MongoDB
```dockerfile
FROM mongo:7

COPY init.js /docker-entrypoint-initdb.d/

EXPOSE 27017
```
- Arquivo para carga de dados (`init.js`)
```javascript
db = db.getSiblingDB('imobiliaria');

db.imoveis.insertMany([
  { endereco: "Rua A, 123", cidade: "São Paulo", valor: 750000, metragem: 120, cpf_proprietario: "111.111.111-11" },
  { endereco: "Rua B, 456", cidade: "Rio de Janeiro", valor: 680000, metragem: 95, cpf_proprietario: "222.222.222-22" },
  { endereco: "Rua C, 789", cidade: "Belo Horizonte", valor: 820000, metragem: 140, cpf_proprietario: "333.333.333-33" },
  { endereco: "Rua D, 111", cidade: "Curitiba", valor: 590000, metragem: 88, cpf_proprietario: "444.444.444-44" },
  { endereco: "Rua E, 222", cidade: "Porto Alegre", valor: 610000, metragem: 92, cpf_proprietario: "555.555.555-55" },
  { endereco: "Rua F, 333", cidade: "Salvador", valor: 730000, metragem: 110, cpf_proprietario: "666.666.666-66" },
  { endereco: "Rua G, 444", cidade: "Fortaleza", valor: 540000, metragem: 85, cpf_proprietario: "777.777.777-77" },
  { endereco: "Rua H, 555", cidade: "Recife", valor: 690000, metragem: 100, cpf_proprietario: "888.888.888-88" },
  { endereco: "Rua I, 666", cidade: "Brasília", valor: 880000, metragem: 150, cpf_proprietario: "999.999.999-99" },
  { endereco: "Rua J, 777", cidade: "Manaus", valor: 470000, metragem: 75, cpf_proprietario: "101.101.101-10" },
  { endereco: "Rua P, 404", cidade: "São Paulo", valor: 780000, metragem: 130, cpf_proprietario: "111.111.111-11" },
  { endereco: "Rua Q, 505", cidade: "Rio de Janeiro", valor: 710000, metragem: 105, cpf_proprietario: "222.222.222-22" }
]);
```
- Montagem e execução do container
```bash
docker build -t bd-mongo .
docker run -d -p 27017:27017 --name bd-mongo bd-mongo
```
