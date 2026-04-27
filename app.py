from flask import Flask, request, jsonify
from google.cloud import storage, bigquery
import pandas as pd
import io

app = Flask(__name__)

PROJECT_ID = "SEU_PROJECT_ID"
DATASET = "musicas"
TABLE = "musicas_curadas"


@app.route("/processar", methods=["POST"])
def processar():
    data = request.get_json()

    bucket_name = data["bucket"]
    file_name = data["file"]

    # -----------------------------
    # Ler arquivo do Cloud Storage
    # -----------------------------
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    csv_data = blob.download_as_bytes()

    df = pd.read_csv(io.BytesIO(csv_data), sep=";")

    linhas_originais = len(df)

    # -----------------------------
    # COMPLETENESS
    # -----------------------------
    df = df[
        df["nome_musica"].notna() &
        df["nome_artista"].notna()
    ]

    # -----------------------------
    # VALIDITY
    # -----------------------------
    df["data_execucao"] = pd.to_datetime(
        df["data_execucao"],
        errors="coerce"
    )

    df = df[df["data_execucao"].notna()]

    # -----------------------------
    # CONSISTENCY
    # -----------------------------
    df = df[(df["nota"] >= 0) & (df["nota"] <= 10)]

    linhas_validas = len(df)
    linhas_descartadas = linhas_originais - linhas_validas

    # -----------------------------
    # BigQuery
    # -----------------------------
    client = bigquery.Client()

    table_id = f"{PROJECT_ID}.{DATASET}.{TABLE}"

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE"
    )

    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=job_config
    )

    job.result()

    return jsonify({
        "status": "ok",
        "linhas_originais": int(linhas_originais),
        "linhas_validas": int(linhas_validas),
        "linhas_descartadas": int(linhas_descartadas)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```
