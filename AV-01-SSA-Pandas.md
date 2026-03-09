### AV-01-SSA-Pandas
- Utilizando `pandas` e `request` preparar o *CSV* disponível em `https://raw.githubusercontent.com/esensato/ssa-2026-01/refs/heads/main/carros-fipe.csv` para ingestão em um *pipeline* de dados conforme os requisitos abaixo:
    - Acessar o ambiente [Colab](https://colab.research.google.com/)
    - Obter o *CSV* `carros-fipe.csv` que possui as colunas:
        - `registro_id`: número sequencial que deve ser **eliminada** (remover a coluna do *Dataset*)
        - `marca_id`: número indicando a marca do veículo
        - `modelo_id`: número indicando o modelo do veículo
        - `ano_modelo`: ano do veículo (deve estar do padrão `aaaa-nn` onde `aaaa` corresponde ao ano e `nn` a um número sequencial separados por **-**)
        - `data_venda`: data em que o veículo foi vendido (padrão `dd/mm/aaaa`)
        - `valor_venda`: valor da venda do veículo (padrão `nnnn,nn`, por exemplo, `45000,00`)
        - `taxa_servico`: taxa de corretagem para a venda (padrão `nnnn,nn`, por exemplo, `500,00`)
        - `valor_total`: total venda calculado por `valor_venda + taxa_servico`
        - `km_rodados`: número indicando a quilometragem do veículo (deve conter somente números)
        - `placa`: placa do veículo campo obrigatório (deve conter somente letras e números)
        - `cliente`: nome do cliente
        - `cpf`: cpf do cliente somente com números e deve ser obrigatório
        - `estado`: estado de registro do veículo
    - Identificar os problemas no *Dataset*
    - Efetuar as devidas correções e descartes (quando campo for obrigatório)
    - Obter o preço do veículo e armazenar em uma nova coluna `preco_fipe` consultando o *endpoint*
        - `https://parallelum.com.br/fipe/api/v1/carros/marcas/marca_id/modelos/modelo_id/anos/ano_modelo`, substituindo `marca_id`, `modelo_id` e `ano_modelo`
        - A nova coluna `preco_fipe` deve conter o valor retornado pelo *endpoint* (*JSON*) no atributo `Valor` (manter somente números e separador de centavos como ",")
        - Incluir também uma coluna marca que deve conter o retorno ao *endpoint* acima a partir do atributo `Marca`
        - Criar uma nova coluna `lucro` com a diferença entre `preco_fipe` e `valor_venda`
        - Descartar os registros que não retornem resultados (armazenar no arquivo `carros-fipe-descarte-endpoint.csv`)
    - Gerar um arquivo `carros-fipe-saida.csv`
    - Gerar um arquivo `carros-fipe-descarte.csv` com as linhas que foram eliminadas
    - Gerar um arquivo `carros-fipe-descarte-endpoint.csv` com os descartes por conta da consulta ao *endpoint* para obter o `preco_fipe`
    - Gerar um arquivo `total_por_marca.csv` contendo o *pivotamento* da nova coluna `marca` (linhas) e `ano` (colunas) exibindo o valor total vendido por marca x ano:

    | marca    | 2018   | 2019   | 2020   | 2021  |
    | -------- | ------ | ------ | ------ | ----- |
    | FIAT     | 120000 | 90000  | 150000 | 80000 |
    | FORD     | 70000  | 100000 | 110000 | 60000 |

    - Atenção!!! Trocar o atributo `cliente` da primeira linha do *dataset* pelo **seu nome**
#### Quando Finalizar
- Anexar o `.ipynb` (menu Arquivo -> Fazer Download -> Baixar o `.ipynb`) junto à atividade do **Canvas**
- Anexar os arquivos `carros-fipe-saida.csv`, `carros-fipe-descarte.csv`, `total_por_marca.csv` e `carros-fipe-descarte-endpoint.csv`
