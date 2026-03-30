import sys
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

engine = create_engine(
    "postgresql+psycopg2://grafana:grafana@localhost:5432/metrics"
)

def buscar_tipos_exame(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, tipo FROM tipo_exame")
        resultados = cursor.fetchall()
        return resultados

    except Exception as e:
        print("Erro ao consultar:", e)
        return []

    finally:
        cursor.close()

def zerar_metricas():
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM data_quality_metrics"))
        conn.commit()

def inserir_metricas(completeness, validity, consistency, uniqueness, accuracy, timeliness, total_registros):
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
    ) VALUES (:data_execucao, :completeness, :validity, :consistency, :uniqueness, :accuracy, :timeliness, 0, :total_registros)
    """

    params = {"data_execucao": datetime.now(), 
              "completeness": float(completeness),
              "validity": float(validity),
              "consistency": float(consistency),
              "uniqueness": float(uniqueness),
              "accuracy": float(accuracy),
              "timeliness": float(timeliness),
              "total_registros": total_registros}

    with engine.connect() as conn:
        conn.execute(text(insert_sql), params)
        conn.commit()

# COLETA DE METRICAS
# As metricas sempre irao refletir o pior caso, em termos percentuais
# campos_falta = 12, total_registros = 15, 12 / 15 = 0,8 (80% ferem o criterio de completude)

# Campos obrigatorios: exame_id, data_exame, custo_exame e paciente_id
def completude_geral(df):
    exame_id = df["exame_id"].isna().sum()
    data_exame = df["data_exame"].isna().sum()
    custo_exame = df["custo_exame"].isna().sum()
    paciente_id = df["paciente_id"].isna().sum()
    quantidade = exame_id + data_exame + custo_exame + paciente_id
    return round(100 * (quantidade / len(df)), 2)

# Acuracia em relacao ao tipo de exame (armazenados em banco de dados, tabela tipo_exame)
def verificar_tipo_exame(df):
    df_tipo_exame = pd.read_sql("SELECT id, tipo FROM tipo_exame", engine)
    quantidade = (~df["tipo_exame"].isin(df_tipo_exame["tipo"])).sum()
    return round(100 * (quantidade / len(df)), 2)

# Nao podem ocorrer pagamentos particulares e por meio do plano de saude
# para um mesmo exame
def pagamento_inconsistente(df):
    quantidade = (df["valor_plano"].notna() & df["valor_particular"].notna()).sum()
    return round(100 * (quantidade / len(df)), 2)

# Validade em relacao ao padrao de paciente_id (PNNN)
def verificar_padrao_paciente_id(df):
    novo_df = df[~df["paciente_id"].isna()]
    quantidade = len(novo_df) - novo_df["paciente_id"].astype(str).str.match(r"^P\d{3}$").sum()
    return round(100 * (quantidade / len(df)), 2)

# Quantidade de linhas inteiras duplicadas
def verificar_unicidade(df):
    quantidade = df.duplicated().sum()    
    return round(100 * (quantidade / len(df)), 2)

# Avalia a idade do dataset tomando a diferenca de dias entre a data atual
# e o registro mais recente do dataset (coluna data_exame)
def registro_mais_recente(df):
    datas = pd.to_datetime(df["data_exame"], errors='coerce')    
    hoje = pd.Timestamp.now()
    diferenca = (hoje - datas).dt.days
    diferenca_dias = diferenca > 10
    return round(100 * (diferenca_dias.sum() / len(df)), 2)

# Coleta as metricas
def coletar_metricas(arquivo_csv):
    df = pd.read_csv(arquivo_csv)
    completeness = completude_geral(df)
    validity = verificar_padrao_paciente_id(df)
    consistency = pagamento_inconsistente(df)
    uniqueness = verificar_unicidade(df)
    accuracy = verificar_tipo_exame(df)
    timeliness = registro_mais_recente(df)
    total_registros = len(df)

    print(f"- Completeness: {completeness}")
    print(f"- Validity: {validity}")
    print(f"- Consistency: {consistency}")
    print(f"- Uniqueness: {uniqueness}")
    print(f"- Accuracy: {accuracy}")
    print(f"- Timeliness: {timeliness}")

    inserir_metricas(completeness, validity, consistency, uniqueness, accuracy, timeliness, total_registros);

    print ("Metricas inseridas no banco de dados!")
    
# Inicio do script - aceita um parametro que pode ser:
# - nome do arquivo .csv para processamento
# - zerar: apaga as metricas ja registradas no banco de dados
def main():
    if (len(sys.argv) > 1):
        if (sys.argv[1] == 'zerar'):
            zerar_metricas()
        else:
            coletar_metricas(sys.argv[1])
    else:
        print("Informe o caminho do arquivo de entrada como parâmetro!")

if __name__ == "__main__":
    main()
