# Importações básicas

import pandas as pd
import streamlit as st

# Importações do modelo

from joblib import load
from notebooks.src.config import DADOS_TRATADOS, MODELO_FINAL


# Funcões básicas
@st.cache_data
def carregar_dados():
    return pd.read_parquet(DADOS_TRATADOS)

@st.cache_resource
def carregar_modelo():
    return load(MODELO_FINAL)

# Variáveis básicas
df = carregar_dados()
modelo = carregar_modelo()

# Variáveis auxiliares de nomeclatura

dic_niveis_educacionais = {
    # 1: "Formação Básica",
    # 2: "Ensino Superior Incompleto",
    # 3: "Ensino Superior Completo",
    # 4: "Mestre",
    # 5: "Doutor",

    1: "Below College",
    2: "College",
    3: "Bachelor",
    4: "Master",
    5: "PhD",

}

dic_nives_de_satisfacao = {
    # 1: 'Baixo',
    # 2: 'Médio',
    # 3: 'Alto',
    # 4: 'Muito alto',

    1: "Low",
    2: "Medium",
    3: "High",
    4: "Very High",
}

dic_niveis_vida_trabalho = {
    # 1: 'Ruim',
    # 1: 'Bom',
    # 1: 'Melhor',
    # 1: 'Muito melhor',

    1: "Bad",
    2: "Good",
    3: "Better",
    4: "Best",
}


# Variáveis auxiliares de objetovs no site (caixas, sliders e outros)

generos = sorted(df["Gender"].unique())
niveis_educacionais = sorted(df["Education"].unique())
area_formacao = sorted(df["EducationField"].unique())
departamentos = sorted(df["Department"].unique())
viagem_negocios = sorted(df["BusinessTravel"].unique())
hora_extra = sorted(df["OverTime"].unique())
satisfacao_trabalho = sorted(df["JobSatisfaction"].unique())
satisfacao_colegas = sorted(df["RelationshipSatisfaction"].unique())
satisfacao_ambiente = sorted(df["EnvironmentSatisfaction"].unique())
vida_trabalho = sorted(df["WorkLifeBalance"].unique())
opcao_acoes = sorted(df["StockOptionLevel"].unique())
envolvimento_trabalho = sorted(df["JobInvolvement"].unique())


colunas_slider = [
    "DistanceFromHome",
    "MonthlyIncome",
    "NumCompaniesWorked",
    "PercentSalaryHike",
    "TotalWorkingYears",
    "TrainingTimesLastYear",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager",
]

colunas_slider_min_max = {
    coluna: {"min_value": df[coluna].min(), "max_value": df[coluna].max()}
    for coluna in colunas_slider
}

colunas_ignoradas = ( 
    # colunas necessárias para entrada do modelo, porém sem impacto na previsão
    
    "Age",
    "DailyRate",
    "JobLevel",
    "HourlyRate",
    "MonthlyRate",
    "PerformanceRating",
)

med_colunas_ignoradas = {
    c : df[c].median() for c in colunas_ignoradas
}


# Código do site

## Configuração da página
st.set_page_config(
    page_title="Previsão de Atrito",
    layout="wide", 
    initial_sidebar_state="auto"
)

## Configuração dos campos

st.title("Previsão de atrito")

col_geral_esq, col_geral_dir = st.columns(2)

with col_geral_esq:

    with st.container(border=True):
        st.write("### Informações pessoais")

        col_es_inf, col_di_inf = st.columns(2)

        with col_es_inf:
            widget_genero = st.radio("Gênero", generos)

        with col_di_inf:
            widget_area_formacao = st.selectbox("Area de Formação", area_formacao)
            widget_nivel_educacional = st.selectbox(
                "Nível Educacional", niveis_educacionais,
                format_func= lambda numero: dic_niveis_educacionais[numero]
            )

        widget_dist_casa = st.slider("Distância de casa (em milhas)", **colunas_slider_min_max['DistanceFromHome'])

    with st.container(border=True):
        st.write("### Rotina na empresa")

        col_es, col_di = st.columns(2)

        with col_es:

            widget_depto = st.selectbox("Departamento", departamentos)
            widget_via_neg = st.selectbox("Viagem de Negócios", viagem_negocios)

        with col_di:
            widget_cargo = st.selectbox(
                "Cargo",
                sorted(df[
                    df["Department"] == widget_depto
                    ]["JobRole"].unique()
                )
            )

            widget_hr_ext = st.radio("Horas Extras", hora_extra)

        widget_salario_mensal = st.slider(
            "Salário Mensal", **colunas_slider_min_max['MonthlyIncome']
        )

with col_geral_dir:

    with st.container(border=True):
        st.write("### Experiência profissional")

        col_es_exp, col_di_exp = st.columns(2)

        with col_es_exp:

            widget_empresas_trabalhadas = st.slider(
                "Empresas trabalhadas", **colunas_slider_min_max["NumCompaniesWorked"]

            )

            widget_anos_trabalhadas = st.slider(
                "Anos Trabalhados" , **colunas_slider_min_max["TotalWorkingYears"]
            )

            widget_anos_empresa = st.slider(
                "Anos na Empresa" , **colunas_slider_min_max["YearsAtCompany"]
            )

        with col_di_exp:

            widget_anos_cargo_atual = st.slider(
                "Anos no Cargo Atual", **colunas_slider_min_max["YearsInCurrentRole"]
            )

            widget_anos_mesmo_gerente = st.slider(
                "Anos com o Mesmo Gerente", **colunas_slider_min_max["YearsWithCurrManager"]
            )

            widget_anos_ultima_promocao = st.slider(
                "Anos Desde a Última Promoção", **colunas_slider_min_max["YearsSinceLastPromotion"]
            )

    with st.container(border=True):
        st.write("### Métricas")

        col_es_inc, col_di_inc = st.columns(2)

        with col_es_inc:

            widget_satisfacao_trabalho = st.selectbox(
                "Satisfação no Trabalho", satisfacao_trabalho,
                format_func= lambda n: dic_nives_de_satisfacao[n]
            )

            widget_satisfacao_colegas = st.selectbox(
            "Satisfação com Colegas",
            satisfacao_colegas,
            format_func=lambda numero: dic_nives_de_satisfacao[numero],
        )
            
            widget_envolvimento_trabalho = st.selectbox(
                "Envolvimento no Trabalho", envolvimento_trabalho
            )

    
        with col_di_inc:
            widget_satisfacao_ambiente_trabalho = st.selectbox(
                "Satisfação no Ambiente de Trabalho", satisfacao_ambiente,
                format_func= lambda n: dic_nives_de_satisfacao[n]
            )

            widget_balanco_vida_trabalho = st.selectbox(
            "Balanço Vida-Trabalho",
            vida_trabalho,
            format_func=lambda numero: dic_niveis_vida_trabalho[numero],
        )
            widget_treinamentos = st.slider(
                "Treinamentos no Último ano",
                **colunas_slider_min_max['TrainingTimesLastYear']
            )
            
with st.container(border=True):
    st.write("### Incentivos")
        
    widget_opcao_acoes = st.radio("Opção de Ações", opcao_acoes,
                                    horizontal=True)
    
    widget_aum_sal = st.slider(
        "Aumento Salarial (%)",
        **colunas_slider_min_max['PercentSalaryHike']
    )
 
## Código "back-end" de previsão

entrada_modelo = {
    "Age": med_colunas_ignoradas["Age"],
    "BusinessTravel": widget_via_neg,
    "DailyRate": med_colunas_ignoradas["DailyRate"],
    "Department": widget_depto,
    "DistanceFromHome": widget_dist_casa,
    "Education": widget_nivel_educacional,
    "EducationField": widget_area_formacao,
    "EnvironmentSatisfaction": widget_satisfacao_ambiente_trabalho,
    "Gender": widget_genero,
    "HourlyRate": med_colunas_ignoradas["HourlyRate"],
    "JobInvolvement": widget_envolvimento_trabalho,
    "JobLevel": med_colunas_ignoradas["JobLevel"],
    "JobRole": widget_cargo,
    "JobSatisfaction": widget_satisfacao_trabalho,
    "MaritalStatus": "Single",
    "MonthlyIncome": widget_salario_mensal,
    "MonthlyRate": med_colunas_ignoradas["MonthlyRate"],
    "NumCompaniesWorked": widget_empresas_trabalhadas,
    "PerformanceRating": med_colunas_ignoradas["PerformanceRating"],
    "OverTime": widget_hr_ext,
    "PercentSalaryHike": widget_aum_sal,
    "RelationshipSatisfaction": widget_satisfacao_colegas,
    "StockOptionLevel": widget_opcao_acoes,
    "TotalWorkingYears": widget_anos_trabalhadas,
    "TrainingTimesLastYear": widget_treinamentos,
    "WorkLifeBalance": widget_balanco_vida_trabalho,
    "YearsAtCompany": widget_anos_empresa,
    "YearsInCurrentRole": widget_anos_cargo_atual,
    "YearsSinceLastPromotion": widget_anos_ultima_promocao,
    "YearsWithCurrManager": widget_anos_mesmo_gerente,
}

df_entrada_modelo = pd.DataFrame([entrada_modelo])


botao_previsao = st.button("Fazer Previsão")

if botao_previsao:

    previsao = modelo.predict(df_entrada_modelo)[0]

    prob_atr = modelo.predict_proba(df_entrada_modelo)[0][1]

    cor = ':red' if previsao == 1 else ':green'

    texto_proba = (
        f"### Probabilidade de Atrito: {cor}[{prob_atr:.2%}]"
    )
    texto_classe = (
        f"### Atrito: {cor}[{"Sim" if previsao == 1 else "Não"}]"
    )

    st.markdown(texto_classe)
    st.markdown(texto_proba)
