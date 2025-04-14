"""
This is a boilerplate pipeline 'aplicacao'
generated using Kedro 0.19.12
"""
import pandas as pd
import mlflow.sklearn
from sklearn.metrics import log_loss, f1_score

def aplicar_modelo(dataset_prod: pd.DataFrame, params: dict):
    """
    Carrega o modelo registrado via MLflow, aplica-o na base de produção e calcula as métricas.
    
    Parâmetros:
        dataset_prod: DataFrame contendo a base de produção.
        params: Dicionário com os parâmetros necessários, incluindo:
                - "selected_columns": lista de colunas a serem utilizadas.
                - "model_uri": URI do modelo registrado.
                
    Retorna:
        resultados: DataFrame com os dados originais (apenas das colunas definidas) acrescidos da predição 
                    e da probabilidade da classe positiva.
        metrics: Dicionário contendo o novo log loss e f1_score.
    """
    # Seleciona somente as colunas definidas no parameters.yml
    selected_columns = params["selected_columns"]
    dataset_prod = dataset_prod[selected_columns].dropna()
    
    # Carrega o modelo via MLflow utilizando a URI definida nos parâmetros
    model_uri = params["model_uri"]   # Exemplo: "models:/modelo_final/2"
    modelo = mlflow.sklearn.load_model(model_uri)
    
    # Separa as features (X) e a coluna alvo (y)
    y_true = dataset_prod["shot_made_flag"]
    X = dataset_prod.drop(columns=["shot_made_flag"])
    
    # Realiza as predições
    y_pred = modelo.predict(X)
    y_pred_proba = modelo.predict_proba(X)
    
    # Cria um DataFrame de resultados, incluindo as predições e a probabilidade da classe positiva
    resultados = dataset_prod.copy()
    resultados["prediction"] = y_pred
    resultados["probability"] = y_pred_proba[:, 1]
    
    # Calcula as métricas: log loss e f1_score
    log_loss_val = log_loss(y_true, y_pred_proba)
    f1_val = f1_score(y_true, y_pred)

    # Loga as métricas no MLflow
    mlflow.log_metric("log_loss_aplicacao", log_loss_val)
    mlflow.log_metric("f1_score_aplicacao", f1_val)
    
    metrics = {
        "log_loss_aplicacao": log_loss_val,
        "f1_score_aplicacao": f1_val
    }
    
    return {"resultados_aplicacao": resultados, "metrics_aplicacao": metrics, "metrics_aplicacao_json": metrics}
