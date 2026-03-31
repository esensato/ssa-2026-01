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
      PGADMIN_CONFIG_WTF_CSRF_ENABLED: "False"
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
- Abrir o navegador na porta `3000` (**Grafana**) e informar o usuário e senha `admin` / `admin`
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
### Criar o Schema
- Configurar a conexão com o **pgadmin** informando o *hostname* **postgres**
- Criar a tabela para armazenar as métricas de qualidade
```sql
CREATE TABLE data_quality_metrics (
    id SERIAL PRIMARY KEY,
    data_execucao TIMESTAMP,
    completeness NUMERIC(5,2),
    validity NUMERIC(5,2),
    consistency NUMERIC(5,2),
    uniqueness NUMERIC(5,2),
    accuracy NUMERIC(5,2),
    timeliness NUMERIC(5,2),
    integrity NUMERIC(5,2),
    total_registros INT
);
```
- Função para inserir dados das métricas calculadas
```python
import psycopg2
from datetime import datetime

def inserir_metrica_bd (completeness,
    validity,
    consistency,
    uniqueness,
    accuracy,
    timeliness,
    integrity,
    total):

    conn = psycopg2.connect(
        host="localhost",
        database="metrics",
        user="grafana",
        password="grafana"
    )

    cursor = conn.cursor()

    insert_sql = """
    INSERT INTO data_quality_metrics (
        data_execucao,
        completeness,
        validity,
        consistency,
        uniqueness,
        accuracy,
        timeliness,
        integrity,
        total_registros
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(insert_sql, (
        datetime.now(),
        completeness,
        validity,
        consistency,
        uniqueness,
        accuracy,
        timeliness,
        integrity,
        total
    ))

    conn.commit()
    cursor.close()
    conn.close()
```
### Criação dos Dashboards
- Consulta para *timeline*
```sql
SELECT
  data_execucao AS time,
  completeness,
  validity,
  consistency,
  uniqueness,
  accuracy,
  timeliness,
  integrity
FROM data_quality_metrics
ORDER BY time;
```
- Consulta para *gauge* (exibindo sempre o último valor, por exemplo, *completeness*)
```sql
SELECT completeness
FROM data_quality_metrics
ORDER BY data_execucao DESC
LIMIT 1;
```
### Exercício
- Criar uma tabela para conter os tipos de exame
```sql
CREATE TABLE tipo_exame (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(100)
);
```
- Inserir os tipos
```sql
INSERT INTO tipo_exame (tipo) VALUES ('HEMOGRAMA');
INSERT INTO tipo_exame (tipo) VALUES ('RAIO_X');
INSERT INTO tipo_exame (tipo) VALUES ('ULTRASSOM');
INSERT INTO tipo_exame (tipo) VALUES ('TOMOGRAFIA');
INSERT INTO tipo_exame (tipo) VALUES ('RESSONANCIA');
```
- Obter os `datasets` (no codespaces)
```bash
wget https://raw.githubusercontent.com/esensato/ssa-2026-01/refs/heads/main/exames_hospital_A.csv
wget https://raw.githubusercontent.com/esensato/ssa-2026-01/refs/heads/main/exames_hospital_B.csv
wget https://raw.githubusercontent.com/esensato/ssa-2026-01/refs/heads/main/exames_hospital_C.csv
```
```bash
pip install sqlalchemy psycopg2-binary
```
- Utilizar como base o *script* [metricas.py](https://raw.githubusercontent.com/esensato/ssa-2026-01/refs/heads/main/metricas.py)
- Criar uma tabela para armazenar o total de registros processados, o total de falhas e o total de sucessos e criar 3 *gauges* no **Grafana** para representar os valores na forma de um *dashboard*
### Instalar Airflow
- Criar uma pasta e obter o `docker-compose.yaml` (referência [airflow.apache.org](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html))
```bash
mkdir airflow
cd airflow
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.1.8/docker-compose.yaml'
```
- Abrir o arquivo `docker-compose.yaml` e alterar / incluir
```yaml
AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
AIRFLOW__CORE__EXECUTION_API_SERVER_URL: 'http://localhost:8080/execution/'
# incluir
AIRFLOW__DAG_PROCESSOR__MIN_FILE_PROCESS_INTERVAL: 5 
AIRFLOW__CORE__MIN_SERIALIZED_DAG_UPDATE_INTERVAL: 5
AIRFLOW__CORE__MIN_SERIALIZED_DAG_FETCH_INTERVAL: 5
```
- Criar configurações iniciais
```bash
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
- Iniciar o banco de dados do `airflow`
```bash
docker-compose up airflow-init
```
- Iniciar o **airflow**
```bash
docker-compose up -d
```
- Acesso via linha de comando
```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.1.8/airflow.sh'
chmod +x airflow.sh
./airflow.sh info
```
- Acesso pelo navegador na porta `8080` (se der erro remover o atributo `?next=...`)
- Usuário e senha iniciais: `airflow` / `airflow`
- Testando a primeira **DAG**
```python
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="hello_dag",
    description="DAG Hello World!",
    schedule=None,
    start_date=pendulum.datetime(2026,1,1,tz="America/Sao_Paulo"),
    catchup=False,
    tags=["hello","world"]
) as dag:
    task1 = BashOperator(task_id='task-1', bash_command="sleep 3")
    task2 = BashOperator(task_id='task-2', bash_command="echo Hello DAG!!!")
    task3 = BashOperator(task_id='task-3', bash_command="sleep 5")    
    task4 = BashOperator(task_id='task-4', bash_command="exit 0")  
    task1 >> task2 >> task3 >> task4
```
- Testando uma falha
```python
    task4 = BashOperator(task_id='task-4', bash_command="exit 1", retries=3)
```
### Triggers
- Exemplo `ONE_FAILED`
```python
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.trigger_rule import TriggerRule

with DAG(
    dag_id="trigger_one_failed",
    start_date=pendulum.datetime(2026,1,1,tz="America/Sao_Paulo"),
    schedule=None,
    catchup=False
) as dag:

    sucesso = BashOperator(
        task_id="sucesso",
        bash_command="echo OK"
    )

    falha = BashOperator(
        task_id="falha",
        bash_command="exit 1"
    )

    alerta = BashOperator(
        task_id="alerta",
        bash_command="echo 'Uma task falhou!'",
        trigger_rule=TriggerRule.ONE_FAILED
    )

    [sucesso, falha] >> alerta
```
- Exemplo `ALL_FAILED`
```python
with DAG(
    dag_id="trigger_all_failed",
    start_date=pendulum.datetime(2026,1,1,tz="America/Sao_Paulo"),
    schedule=None,
    catchup=False
) as dag:

    falha1 = BashOperator(
        task_id="falha1",
        bash_command="exit 1"
    )

    falha2 = BashOperator(
        task_id="falha2",
        bash_command="exit 1"
    )

    somente_se_tudo_quebrar = BashOperator(
        task_id="all_failed_task",
        bash_command="echo 'Tudo falhou!'",
        trigger_rule=TriggerRule.ALL_FAILED
    )

    [falha1, falha2] >> somente_se_tudo_quebrar
```
- Exemplo `ONE_SUCESS`
```python
with DAG(
    dag_id="trigger_one_success",
    start_date=pendulum.datetime(2026,1,1,tz="America/Sao_Paulo"),
    schedule=None,
    catchup=False
) as dag:

    ok = BashOperator(
        task_id="ok",
        bash_command="echo OK"
    )

    erro = BashOperator(
        task_id="erro",
        bash_command="exit 1"
    )

    continua = BashOperator(
        task_id="continua",
        bash_command="echo 'Pelo menos uma funcionou!'",
        trigger_rule=TriggerRule.ONE_SUCCESS
    )

    [ok, erro] >> continua
```
- Exemplo `NONE_FAILED`
```python
with DAG(
    dag_id="trigger_none_failed",
    start_date=pendulum.datetime(2026,1,1,tz="America/Sao_Paulo"),
    schedule=None,
    catchup=False
) as dag:

    t1 = BashOperator(
        task_id="t1",
        bash_command="echo OK"
    )

    t2 = BashOperator(
        task_id="t2",
        bash_command="echo OK"
    )

    final = BashOperator(
        task_id="final",
        bash_command="echo 'Nenhuma falhou!'",
        trigger_rule=TriggerRule.NONE_FAILED
    )

    [t1, t2] >> final
```
- Exemplo `ALL_DONE`
```python
with DAG(
    dag_id="trigger_all_done",
    start_date=pendulum.datetime(2026,1,1,tz="America/Sao_Paulo"),
    schedule=None,
    catchup=False
) as dag:

    t1 = BashOperator(
        task_id="t1",
        bash_command="exit 1"
    )

    t2 = BashOperator(
        task_id="t2",
        bash_command="echo OK"
    )

    sempre = BashOperator(
        task_id="sempre_executa",
        bash_command="echo 'Executo sempre!'",
        trigger_rule=TriggerRule.ALL_DONE
    )

    [t1, t2] >> sempre
```
### Principais Operadores
- Exemplo de `ShortCircuitOperator`
```python
import os
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator, ShortCircuitOperator

def verificar_arquivo():
    caminho = "/tmp/dados.csv"
    
    existe = os.path.exists(caminho)
    print(f"Arquivo existe? {existe}")
    
    return existe

def processar():
    print("Processando arquivo...")

def finalizar():
    print("Finalizando pipeline...")

with DAG(
    dag_id="short_circuit_example",
    start_date=pendulum.datetime(2026,1,1,tz="America/Sao_Paulo"),
    schedule=None,
    catchup=False,
    tags=["controle_fluxo"]
) as dag:

    checar = ShortCircuitOperator(
        task_id="verificar_arquivo",
        python_callable=verificar_arquivo
    )

    processar_task = PythonOperator(
        task_id="processar",
        python_callable=processar
    )

    finalizar_task = PythonOperator(
        task_id="finalizar",
        python_callable=finalizar
    )

    checar >> processar_task >> finalizar_task
```
- Exemplo de `SimpleHttpOperator`
```python
import pendulum
from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator

def processar_resposta(**context):
    response = context['ti'].xcom_pull(task_ids='get_posts')
    print("Resposta da API:")
    print(response[:200])  # imprime só parte

with DAG(
    dag_id="http_real_example",
    start_date=pendulum.datetime(2026,1,1,tz="America/Sao_Paulo"),
    schedule=None,
    catchup=False,
    tags=["http","api"]
) as dag:

    get_posts = SimpleHttpOperator(
        task_id="get_posts",
        http_conn_id="jsonplaceholder_api",
        endpoint="/posts",
        method="GET",
        headers={"Content-Type": "application/json"},
        response_filter=lambda response: response.text,
        log_response=True
    )

    processar = PythonOperator(
        task_id="processar_resposta",
        python_callable=processar_resposta
    )

    get_posts >> processar
```
- Exemplo `SQLCheckOperator`
```python
import pendulum
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLCheckOperator

with DAG(
    dag_id="sql_check_example",
    start_date=pendulum.datetime(2026,1,1,tz="America/Sao_Paulo"),
    schedule=None,
    catchup=False,
    tags=["data_quality"]
) as dag:

    check_regra = SQLCheckOperator(
        task_id="check_regra_negocio",
        conn_id="postgres_default",
        sql="""
        SELECT COUNT(*) = 0
        FROM atendimentos
        WHERE valor_plano IS NOT NULL
          AND valor_particular IS NOT NULL
        """
    )
```
- Exemplo `PostgresOperator`
```python
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

def calcular_metricas(**context):
    metrics = {
        "data_execucao": str(pendulum.now("America/Sao_Paulo")),
        "completeness": 95.5,
        "validity": 98.0,
        "consistency": 92.3,
        "uniqueness": 100.0,
        "accuracy": 97.2,
        "timeliness": 88.0,
        "total_registros": 150
    }
    return metrics

with DAG(
    dag_id="postgres_metrics_example",
    start_date=pendulum.datetime(2026,1,1,tz="America/Sao_Paulo"),
    schedule=None,
    catchup=False,
    tags=["postgres","metrics"]
) as dag:

    calcular = PythonOperator(
        task_id="calcular_metricas",
        python_callable=calcular_metricas
    )

    inserir = PostgresOperator(
        task_id="inserir_metricas",
        postgres_conn_id="postgres_default",
        sql="""
        INSERT INTO data_quality_metrics (
            data_execucao,
            completeness,
            validity,
            consistency,
            uniqueness,
            accuracy,
            timeliness,
            integrity,
            total_registros
        ) VALUES (
            '{{ ti.xcom_pull(task_ids="calcular_metricas")["data_execucao"] }}',
            {{ ti.xcom_pull(task_ids="calcular_metricas")["completeness"] }},
            {{ ti.xcom_pull(task_ids="calcular_metricas")["validity"] }},
            {{ ti.xcom_pull(task_ids="calcular_metricas")["consistency"] }},
            {{ ti.xcom_pull(task_ids="calcular_metricas")["uniqueness"] }},
            {{ ti.xcom_pull(task_ids="calcular_metricas")["accuracy"] }},
            {{ ti.xcom_pull(task_ids="calcular_metricas")["timeliness"] }},
            0,
            {{ ti.xcom_pull(task_ids="calcular_metricas")["total_registros"] }}
        );
        """
    )

    calcular >> inserir
```
- Exemplo `FileSensor`
```python
import pendulum
from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator

def processar_arquivo():
    print("Arquivo encontrado! Processando dados...")

with DAG(
    dag_id="file_sensor_example",
    start_date=pendulum.datetime(2026,1,1,tz="America/Sao_Paulo"),
    schedule=None,
    catchup=False,
    tags=["sensor","file"]
) as dag:

    espera_arquivo = FileSensor(
        task_id="espera_arquivo",
        filepath="/tmp/dados.csv",
        poke_interval=10,   # verifica a cada 10s
        timeout=60,         # falha após 60s
        mode="poke"         # modo padrão
    )

    processar = PythonOperator(
        task_id="processar_arquivo",
        python_callable=processar_arquivo
    )

    espera_arquivo >> processar
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
import pendulum
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
import pandas as pd

CAMINHO_ARQUIVO = "/opt/airflow/dags/vendas.csv"
CAMINHO_SAIDA = "/opt/airflow/dags/resultado.csv"

with DAG(
    dag_id="vendas_dag",
    description="Vendas",
    schedule=None,
    start_date=pendulum.datetime(2026,1,1,tz="America/Sao_Paulo"),
    catchup=False,
    tags=["pipeline","vendas"]
) as dag:
    def ler_csv():
        df = pd.read_csv(CAMINHO_ARQUIVO)
        return df

    def calcular_total(**context):

        df = context['ti'].xcom_pull(task_ids='ler_csv')
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
