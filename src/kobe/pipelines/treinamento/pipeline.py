"""
This is a boilerplate pipeline 'treinamento'
generated using Kedro 0.19.12
"""
from kedro.pipeline import node, Pipeline, pipeline  # noqa
from .nodes import treinar_modelos, avaliar_modelos, escolher_modelo

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=treinar_modelos,
            inputs="base_train",
            outputs=["modelo_reg", "modelo_arvore"],
            name="treinar_modelos"
        ),
        node(
            func=avaliar_modelos,
            inputs=["base_test", "modelo_reg", "modelo_arvore"],
            outputs={
                "log_loss_regressao": "log_loss_regressao",
                "log_loss_regressao_json": "log_loss_regressao_json",
                "log_loss_arvore": "log_loss_arvore",
                "log_loss_arvore_json": "log_loss_arvore_json",
                "f1_score_arvore": "f1_score_arvore",
                "f1_score_arvore_json": "f1_score_arvore_json"
            },
            name="avaliar_modelos"
        ),
        node(
            func=escolher_modelo,
            inputs=["modelo_reg", "modelo_arvore", "log_loss_regressao_json", "log_loss_arvore_json"],
            outputs="modelo_final",
            name="escolher_modelo_final"
        )
    ])
