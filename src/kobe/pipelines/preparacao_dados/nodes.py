"""
This is a boilerplate pipeline 'preparacao_dados'
generated using Kedro 0.19.12
"""
import pandas as pd
from sklearn.model_selection import train_test_split


def selecionar_e_filtrar_dados(
    dataset_dev: pd.DataFrame,
    dataset_prod: pd.DataFrame,
    params: dict ) :
    """
    Seleciona colunas relevantes e remove linhas com valores ausentes.
    """
    colunas = params["selected_columns"]
    df = pd.concat([dataset_dev, dataset_prod], axis=0)[colunas]
    df_filtrado = df.dropna()

    return df_filtrado

    
def dividir_dados(
    df_filtrado: pd.DataFrame,
    params: dict ):
    """
    Realiza a divisão estratificada dos dados em treino e teste.
    """
    test_size = params["test_size"]
    random_state = params["random_state"]

    X = df_filtrado.drop(columns=["shot_made_flag"])
    y = df_filtrado["shot_made_flag"]
    X["shot_made_flag"] = y  # mantém o target no output

    train, test = train_test_split( 
        X,
        test_size=test_size,
        stratify=y,
        random_state=random_state
    )

    return train, test, len(train), len(test)
