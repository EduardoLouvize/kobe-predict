"""
This is a boilerplate pipeline 'treinamento'
generated using Kedro 0.19.12
"""
from pycaret.classification import setup, create_model, predict_model, finalize_model
from sklearn.metrics import log_loss, f1_score
import pandas as pd


def treinar_modelos(base_train: pd.DataFrame):
    # Setup para classificação
    s = setup(data=base_train, target='shot_made_flag', html=False, session_id=42)

    # Criar modelos
    modelo_reg = create_model("lr")    # Regressão logística
    modelo_arvore = create_model("dt") # Árvore de decisão

    # Finaliza ambos os modelos para uso em produção
    modelo_reg_final = finalize_model(modelo_reg)
    modelo_arvore_final = finalize_model(modelo_arvore)

    return modelo_reg_final, modelo_arvore_final


def avaliar_modelos(base_test, modelo_reg, modelo_arvore):
    y_true = base_test["shot_made_flag"]
    X_test = base_test.drop(columns=["shot_made_flag"])

    y_pred_proba_reg = modelo_reg.predict_proba(X_test)
    y_pred_proba_arvore = modelo_arvore.predict_proba(X_test)
    y_pred_arvore = modelo_arvore.predict(X_test)

    log_loss_reg = log_loss(y_true, y_pred_proba_reg)
    log_loss_dt = log_loss(y_true, y_pred_proba_arvore)
    f1_dt = f1_score(y_true, y_pred_arvore)

    return {
        "log_loss_regressao": log_loss_reg,
        "log_loss_regressao_json": log_loss_reg,
        "log_loss_arvore": log_loss_dt,
        "log_loss_arvore_json": log_loss_dt,
        "f1_score_arvore": f1_dt,
        "f1_score_arvore_json": f1_dt
    }


def escolher_modelo(modelo_reg, modelo_arvore, log_loss_reg, log_loss_arvore):
    # Selecionar o melhor modelo com base no menor log_loss
    if log_loss_reg <= log_loss_arvore:
        return modelo_reg
    else:
        return modelo_arvore
