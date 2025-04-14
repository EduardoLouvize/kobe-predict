import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc

def plot_shot_chart(df):
    """
    Plota um gráfico de dispersão (scatter plot) das posições dos lançamentos.
    - Lançamentos feitos: marcados em azul.
    - Lançamentos errados: marcados em vermelho.
    
    Parâmetros:
        df: DataFrame que contenha as colunas 'lat', 'lon' e 'shot_made_flag'.
    """
    # Filtra os lançamentos de acordo com o resultado do shot_made_flag
    acertos = df[df["shot_made_flag"] == 1]
    erros = df[df["shot_made_flag"] == 0]

    fig, ax = plt.subplots()
    # Plota acertos em azul
    ax.scatter(acertos["lon"], acertos["lat"], color="blue", alpha=0.6, label="Acertou")
    # Plota erros em vermelho
    ax.scatter(erros["lon"], erros["lat"], color="red", alpha=0.6, label="Errou")
    
    ax.set_title("Posição dos Lançamentos de Kobe")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.legend()
    
    return fig


def main():
    st.title("Dashboard de Monitoramento da Operação")
    
    # Seção de métricas
    st.header("Métricas de Avaliação")
    try:
        with open("data/07_model_output/metrics_aplicacao.json", "r") as f:
            metrics = json.load(f)
        st.metric("Log Loss", metrics.get("log_loss_aplicacao", "N/A"))
        st.metric("F1 Score", metrics.get("f1_score_aplicacao", "N/A"))
    except Exception as e:
        st.error("Erro ao carregar métricas: " + str(e))
    
    # Seção de resultados da aplicação
    st.header("Resultados da Aplicação")
    try:
        df_resultados = pd.read_parquet("data/07_model_output/resultados_aplicacao.parquet")
        st.subheader("Visualização dos primeiros registros")
        st.write(df_resultados.head())
        st.subheader("Tabela Completa")
        st.dataframe(df_resultados)
    except Exception as e:
        st.error("Erro ao carregar os resultados: " + str(e))
    
    # Seção: Comparação entre predições e valores reais
    st.header("Comparação entre Predições e Valores Reais")
    try:
        df_resultados["acertou"] = df_resultados["prediction"] == df_resultados["shot_made_flag"]
        counts = df_resultados["acertou"].value_counts()
        st.write("Distribuição de acertos vs. erros")
        st.bar_chart(counts)
    except Exception as e:
        st.error("Erro ao criar gráfico de comparação: " + str(e))
    
    # Seção: Matriz de Confusão
    st.header("Matriz de Confusão")
    try:
        if "shot_made_flag" in df_resultados.columns and "prediction" in df_resultados.columns:
            y_true = df_resultados["shot_made_flag"]
            y_pred = df_resultados["prediction"]
            cm = confusion_matrix(y_true, y_pred)
            fig, ax = plt.subplots()
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
            ax.set_xlabel("Predito")
            ax.set_ylabel("Real")
            ax.set_title("Matriz de Confusão")
            st.pyplot(fig)
        else:
            st.warning("Colunas 'shot_made_flag' ou 'prediction' não encontradas no dataset.")
    except Exception as e:
        st.error("Erro ao gerar a matriz de confusão: " + str(e))
    
    # Seção: Curva ROC
    st.header("Curva ROC")
    try:
        # Presume que o dataframe possui a coluna com as probabilidades da classe positiva chamada 'probability'
        if "shot_made_flag" in df_resultados.columns and "probability" in df_resultados.columns:
            y_true = df_resultados["shot_made_flag"]
            y_proba = df_resultados["probability"]
            fpr, tpr, thresholds = roc_curve(y_true, y_proba)
            roc_auc = auc(fpr, tpr)

            fig2, ax2 = plt.subplots()
            ax2.plot(fpr, tpr, label=f'AUC = {roc_auc:.2f}')
            ax2.plot([0, 1], [0, 1], linestyle='--', color='gray')
            ax2.set_xlabel("Taxa de Falsos Positivos")
            ax2.set_ylabel("Taxa de Verdadeiros Positivos")
            ax2.set_title("Curva ROC")
            ax2.legend(loc="lower right")
            st.pyplot(fig2)
        else:
            st.warning("Coluna 'probability' ou 'shot_made_flag' não encontrada para calcular a curva ROC.")
    except Exception as e:
        st.error("Erro ao gerar a curva ROC: " + str(e))
    
    # Seção: Histograma de Probabilidades
    st.header("Distribuição das Probabilidades Preditadas")
    try:
        if "probability" in df_resultados.columns:
            fig3, ax3 = plt.subplots()
            ax3.hist(df_resultados["probability"], bins=20, edgecolor="black")
            ax3.set_xlabel("Probabilidade (classe positiva)")
            ax3.set_ylabel("Frequência")
            ax3.set_title("Histograma das Probabilidades Preditadas")
            st.pyplot(fig3)
        else:
            st.warning("Coluna 'probability' não encontrada para gerar histograma.")
    except Exception as e:
        st.error("Erro ao gerar o histograma: " + str(e))


    st.header("Dashboard de Monitoramento - Lançamentos de Kobe")    
    
    try:
        df = pd.read_parquet("data/07_model_output/resultados_aplicacao.parquet")
        st.dataframe(df.head())
        
        # Plota o gráfico de posições dos lançamentos
        st.header("Mapa de Lançamentos de Kobe")
        fig = plot_shot_chart(df)
        st.pyplot(fig)
        
    except Exception as e:
        st.error("Erro ao carregar os dados ou gerar o gráfico: " + str(e))





if __name__ == "__main__":
    main()
