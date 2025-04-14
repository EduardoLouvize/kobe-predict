"""
This is a boilerplate pipeline 'aplicacao'
generated using Kedro 0.19.12
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa
from .nodes import aplicar_modelo

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=aplicar_modelo,
            inputs=dict(
                dataset_prod="dataset_kobe_prod",
                params="params:aplicacao"  
            ),
            outputs={
                "resultados_aplicacao": "resultados_aplicacao", 
                "metrics_aplicacao": "metrics_aplicacao",
                "metrics_aplicacao_json": "metrics_aplicacao_json"
                },
            name="aplicar_modelo_node"
        )
    ])
