## AV-03-SSA-GCloud
- O objetivo da atividade será migrar para a infraestrutura do **Google Cloud** o projeto já desenvolvido *on-premise* com o **Airflow**
- A resolução deve ser baseada no roteiro das aulas de [Google Cloud](https://github.com/esensato/ssa-2026-01/blob/main/README.md#google-cloud)
- Criar um novo projeto chamado `av-03-ssa`
- Criar as tabelas necessárias no `BigQuery`
```sql
CREATE TABLE genero_musical (
    id_genero VARCHAR(3),
    nome_genero VARCHAR(50)
);

CREATE TABLE descartados (
    total INTEGER NOT NULL
);
```
- Carregar os dados abaixo na tabela `genero_musical`
```sql
cat << EOF > genero_musical.csv
'001','POP'
'002','ROCK'
'003','RAP'
'004','SOUL'
'005','OUTROS'
EOF
```
- Obter o arquivo para se processado
```bash
wget https://raw.githubusercontent.com/esensato/ssa-2026-01/refs/heads/main/dados-stream.csv
```
- Criar um *buket* [Google Cloud Storage](https://github.com/esensato/ssa-2026-01/blob/main/README.md#google-cloud-storage) e efetuar o upload do arquivo `ados-stream.csv` para ser processado
- Seguir o roteiro abaixo com os *steps* desejadas utilizando o [Google Cloud Workflows](https://github.com/esensato/ssa-2026-01/blob/main/README.md#google-cloud-workflows)
  - **STEP-1**: efetuar o tratamento de datas (deixar todas no formato *dd/mm/aaaa* - algumas estão no formato americano *aaaa-mm-dd*) e salvar a saída em um arquivo `step1.csv`
      - Criar um *endpoint* utilizando [Google Cloud Run](https://github.com/esensato/ssa-2026-01/blob/main/README.md#google-cloud-run)
      - Deve ler o arquivo no *bucket* para efetuar o tratamento das datas
  - **STEP-2**: ler o arquivo `step1.csv` do *bucket*, remover as linhas onde `nome_musica` esteja vazio, gerando o arquivo `step2.csv` e iserindo na tabela `descartados` (criada acima) a quantidade de registros descartados
      - Criar um *endpoint* utilizando [Google Cloud Run](https://github.com/esensato/ssa-2026-01/blob/main/README.md#google-cloud-run)
      - Deve ler o arquivo no *bucket* para efetuar o tratamento da quantidade de registros descartados
  - **STEP-3**: enriquecer o arquivo `step2.csv` criando uma nova coluna chamada `nome_genero` que deve consistir com a tabela `genero_musical` (carregada acima) com base no `id_genero` e gerar a saída `step3.csv`
      - Criar um *endpoint* utilizando [Google Cloud Run](https://github.com/esensato/ssa-2026-01/blob/main/README.md#google-cloud-run)
      - Deve ler o arquivo no *bucket* para efetuar o enriquecimento dos dados
  - **STEP-4**: a partir do arquivo `task3.csv` criar uma saída com a média de avaliação por música e gravar no banco de dados (crie a estrutura de tabela)
      - Criar um *endpoint* utilizando [Google Cloud Run](https://github.com/esensato/ssa-2026-01/blob/main/README.md#google-cloud-run)
  - **STEP-5**: a partir do arquivo `task3.csv` criar uma saída com o total de músicas ouvidas por artista e gravar em banco de dados (crie a estrutura de tabela)
      - Criar um *endpoint* utilizando [Google Cloud Run](https://github.com/esensato/ssa-2026-01/blob/main/README.md#google-cloud-run)
  - **STEP-4** e **STEP-5** devem ser exetutadas em paralelo
  - Criar um *dashboard* no **Google Looker** com um *gauge* para exibir a quantidade de registros descartados (**STEP-2**) e gráficos de barra para exibir os dados coletados nas tabelas dos *steps* **STEP-4** e **STEP-5**
### Entrega
- *Printscreen* do dashboard desenvolvido no **Google Looker**
- Roteiro com as instruções e códigos utilizados na resolução da atividade
- Apresentar individualmente o que foi realizado para o professor (caso não seja apresentado haverá um desconto de 2 pontos na atividade)
  