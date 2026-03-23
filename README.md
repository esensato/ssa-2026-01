# ssa-2026-01
Self Service Analytics
### Ambiente Colab
- Acessar [Colab](https://colab.research.google.com/)
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
- Teste final
```bash
docker exec -it bd-postgres psql -U admin -d imobiliaria
select * from proprietarios;
exit
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
- Teste final
```bash
docker exec -it bd-mongo mongosh
show dbs
use imobiliaria
show collections
db.imoveis.find().pretty()
exit
```
### Acessando Bases com Python
- Instalar pacotes necessários
```bash
pip install sqlalchemy psycopg2-binary
pip install pymongo
pip install pandas
```
- Realizar o *join* com o **Python**
```python
from sqlalchemy import create_engine
from pymongo import MongoClient
import pandas as pd

engine = create_engine("postgresql+psycopg2://admin:admin123@localhost:5432/imobiliaria")
df_proprietarios = pd.read_sql("SELECT * FROM proprietarios", engine)

client = MongoClient("mongodb://localhost:27017/")
db = client["imobiliaria"]

imoveis = list(db.imoveis.find())
df_imoveis = pd.DataFrame(imoveis)

df_imoveis.drop(columns=["_id"], inplace=True)

df_final = df_imoveis.merge(
    df_proprietarios,
    left_on="cpf_proprietario",
    right_on="cpf",
    how="left"
)

print(df_final.head())
```
- Problema encontrado: alguns CPFs podem estar fora de padrão...
```python
def limpar_cpf(cpf):
    return cpf.replace(".", "").replace("-", "")

df_proprietarios["cpf_limpo"] = df_proprietarios["cpf"].apply(limpar_cpf)
df_imoveis["cpf_limpo"] = df_imoveis["cpf_proprietario"].apply(limpar_cpf)

df_final = df_imoveis.merge(
    df_proprietarios,
    on="cpf_limpo",
    how="left"
)
```
### Conectar DB2 na Cloud
- Para referência à API clicar [aqui](https://cloud.ibm.com/apidocs/db2-on-cloud/db2-on-cloud-v4)
- Definir as variáveis para a obter o token de conexão
```python
url = ""
userid = ""
password = ""
deployment_id = ""
```
- Obter o token (exemplo em *python*)
```python
import http.client
import ssl
import json

context = ssl._create_unverified_context()

conn = http.client.HTTPSConnection(url, context=context)

payload = {"userid":userid,"password":password}

headers = {
    'content-type': "application/json",
    'x-deployment-id': deployment_id
    }

conn.request("POST", "/dbapi/v4/auth/tokens", json.dumps(payload), headers)

res = conn.getresponse()
data = res.read()

print(json.loads(data.decode("utf-8"))["token"])

token = json.loads(data.decode("utf-8"))["token"]
```
- Armazenar o *token* em uma variável
- Efetuar uma consulta *SQL* ao banco de dados e obter o `id` da execução (assíncrona)
```python
import http.client
import ssl
import json

context = ssl._create_unverified_context()

conn = http.client.HTTPSConnection(url, context=context)

payload = {"commands":"select * from modelos", "separator":";","stop_on_error":"no"}

headers = {
    'content-type': "application/json",
    'authorization': f"Bearer {token}",
     'x-deployment-id': deployment_id
}

conn.request("POST", "/dbapi/v4/sql_jobs", json.dumps(payload), headers)

res = conn.getresponse()
data = res.read()

print(json.loads(data.decode("utf-8"))["id"])

id = data.decode("utf-8"))["id"]
```
- Obter o restulado final da execução (atualizar o `id`)
```python
import http.client
import ssl
import json

context = ssl._create_unverified_context()

conn = http.client.HTTPSConnection(url, context=context)

headers = {
    'content-type': "application/json",
    'authorization': f"Bearer {token}",
     'x-deployment-id': deployment_id
}

conn.request("GET", f"/dbapi/v4/sql_jobs/{id}", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
```
### Grafana
- Acessar [Codespaces](https://github.com/features/codespaces?locale=pt-BR)
- Criar o arquivo `docker-compose.yaml`
```yaml
services:

  postgres:
    image: postgres:14
    container_name: postgres
    environment:
      POSTGRES_USER: grafana
      POSTGRES_PASSWORD: grafana
      POSTGRES_DB: metrics
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    depends_on:
      - postgres
    environment:
      GF_SECURITY_ADMIN_USER: admin
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - grafana_data:/var/lib/grafana
    restart: always

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: pgadmin
    depends_on:
      - postgres
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    volumes:
      - pgadmin_data:/var/lib/pgadmin
    restart: always

volumes:
  postgres_data:
  grafana_data:
  pgadmin_data:
```
- Criar as imagens e *containers*
```bash
docker-compose up -d
```
- Teste de conexão com **Python** e **PostgreSQL**
- Instalar o pacote `psycopg2-binary`
```bash
pip install psycopg2-binary
```
- Código para teste
```python
import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="metrics",
        user="grafana",
        password="grafana"
    )

    print("Conexão realizada com sucesso!")

    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()

    print("Versão do PostgreSQL:", version)

    cursor.close()
    conn.close()

except Exception as e:
    print("Erro ao conectar:", e)
```
### Exemplo Básico Airflow
```dockerfile
FROM apache/airflow:2.8.1

USER airflow

RUN pip install --no-cache-dir pandas

ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

EXPOSE 8080
```
- Montagem e execução do container
```bash
docker build -t airflow .
docker run -d -p 8080:8080 -v $(pwd)/dags:/opt/airflow/dags -v $(pwd)/dados:/opt/airflow/dados --name airflow airflow standalone
```
- Criar usuário administrador
```bash
docker exec -it airflow airflow users create --username airflow --firstname Airflow --lastname User --role Admin --email airflow@email.com --password airflow
```
- Criar um arquivo de exemplo (`vendas.csv`) com dados de venda dentro do diretório `dados`
```csv
produto,quantidade,preco_unitario
A,2,10
B,1,20
A,3,10
C,4,5
B,2,20
```
- Criar o **DAG** (`pipeline_vendas.py`) dentro do diretório `dags`
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd

CAMINHO_ARQUIVO = "/opt/airflow/dados/vendas.csv"
CAMINHO_SAIDA = "/opt/airflow/dados/resultado.csv"

default_args = {
    "start_date": datetime(2024, 1, 1),
}

with DAG(
    dag_id="pipeline_vendas_simples",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    def ler_csv(**context):
        df = pd.read_csv(CAMINHO_ARQUIVO)
        context["ti"].xcom_push(key="dados", value=df.to_json())

    def calcular_total(**context):
        json_data = context["ti"].xcom_pull(key="dados")
        df = pd.read_json(json_data)

        df["total"] = df["quantidade"] * df["preco_unitario"]

        resultado = (
            df.groupby("produto")["total"]
            .sum()
            .reset_index()
            .rename(columns={"total": "total_vendas"})
        )

        resultado.to_csv(CAMINHO_SAIDA, index=False)

    task1 = PythonOperator(
        task_id="ler_csv",
        python_callable=ler_csv
    )

    task2 = PythonOperator(
        task_id="calcular_total",
        python_callable=calcular_total
    )

    task1 >> task2
```
