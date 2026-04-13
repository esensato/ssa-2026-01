## AV-02-SSA-Airflow
- Acessar o [codespaces](https://github.com/codespaces)
- Instalar o **Airflow** [roteiro](https://github.com/esensato/ssa-2026-01/tree/main?tab=readme-ov-file#instalar-airflow)
- Criar a pasta de dados [roteiro](https://github.com/esensato/ssa-2026-01/tree/main?tab=readme-ov-file#pasta-para-dados)
- Criar as tabelas necessárias
```bash
docker exec -it airflow-postgres-1 bash
psql -U airflow -d airflow
- Copiar e colar os arquivos abaixo
```sql
CREATE TABLE genero_musical (
    id_genero VARCHAR(3) PRIMARY KEY,
    nome_genero VARCHAR(50) NOT NULL
);

CREATE TABLE descartados (
    total INTEGER NOT NULL
);

```
- Carregar dados na tabela
```sql
INSERT INTO genero_musical (id_genero, nome_genero) VALUES
('001', 'POP'),
('002', 'ROCK'),
('003', 'RAP'),
('004', 'SOUL'),
('005', 'OUTROS');
```
- Obter o arquivo para se processado
```bash
cd data
wget https://github.com/esensato/ssa-2026-01/blob/main/dados-stream.csv
```
### Implementação
- A equipe de análise de dados de um novo app de *stream* musical deseja montar um *pipeline* para processar um *dataset* e extrair algumas informações sobre as músicas mais solicitadas pelos seus usuários, os artitas mais requisitados e as músicas mais bem avaliadas
- Para tanto optaram por implementar esse *pipeline* utilizando o **Airflow** para automatizar as atividades
- Sendo assim, seguir o roteiro abaixo com as *tasks* desejadas
  - **TASK-1**: renomear o arquivo `/opt/airflow/data/dados-stream.csv` para `/opt/airflow/data/entrada.csv` (`mv /opt/airflow/data/dados-stream.csv /opt/airflow/data/entrada.csv`)
  - **TASK-2**: efetuar o tratamento de datas (deixar todas no formato dd/mm/aaaa - algumas estão no formato americano aaaa-mm-dd) e salvar a saída em um arquivo `task1.csv`
  - **TASK-3**: ler o arquivo `task1.csv` e remover as linhas onde `nome_musica` esteja vazio, gerando o arquivo `task3.csv` e passando como parâmetro para a `task` seguinte (abaixo) via variável de contexto
  - **TASK-4**: inserir na tabela `descartados` criada acima a quantidade de registros descartados que a `task` acima passou como parâmetro
  - **TASK-5**: enriquecer o arquivo `task3.csv` criando uma nova coluna chamada `nome_genero` que deve consistir com a tabela `genero_musical` (criada acima) com base no `id_genero` e gerar a saída `task4.csv`
  - **TASK-6**: a partir do arquivo `task4.csv` criar uma saída com a média de avaliação por música e o total de músicas ouvidas por artista (arquivos `media_avaliacao.csv` e `total_artista.csv`
### Entrega
- Subir código fonte da **DAG** criada ou link do `repo git`
  
