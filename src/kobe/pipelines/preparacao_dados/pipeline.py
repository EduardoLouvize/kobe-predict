"""
This is a boilerplate pipeline 'preparacao_dados'
generated using Kedro 0.19.12
"""
from kedro.pipeline import Pipeline, node, pipeline
from .nodes import selecionar_e_filtrar_dados, dividir_dados

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=selecionar_e_filtrar_dados,
            inputs=dict(
                dataset_dev="dataset_kobe_dev",
                dataset_prod="dataset_kobe_prod",
                params="params:preparacao_dados"
            ),
            outputs="data_filtered",
            name="node_filtrar_dados"
        ),
        node(
            func=dividir_dados,
            inputs=dict(
                df_filtrado="data_filtered",
                params="params:preparacao_dados"
            ),
            outputs=["base_train", "base_test", "tamanho_treino", "tamanho_teste"],
            name="node_split_dados"
        )
    ])
