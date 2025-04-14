"""Project pipelines."""
from __future__ import annotations

# from kedro.pipeline import Pipeline
# from kobe.pipelines.treinamento import pipeline as treinamento_pipeline
# from kobe.pipelines.preparacao_dados import pipeline as preparacao_dados_pipeline


# def register_pipelines() -> dict[str, Pipeline]:
#     return {
#         "preparacao_dados": preparacao_dados_pipeline.create_pipeline(),
#         "treinamento": treinamento_pipeline.create_pipeline(),
#         "__default__": preparacao_dados_pipeline.create_pipeline() + treinamento_pipeline.create_pipeline()
#     }

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = find_pipelines()
    pipelines["__default__"] = sum(pipelines.values())
    return pipelines
