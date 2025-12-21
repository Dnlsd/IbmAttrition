from pathlib import Path


PASTA_PROJETO = Path(__file__).parent.parent

PASTA_DADOS = PASTA_PROJETO / "dados"
PASTA_MODELOS = PASTA_PROJETO / "modelos"


# coloque abaixo o caminho para os arquivos de dados de seu projeto
DADOS_ORIGINAIS = PASTA_DADOS / "employee_attrition.csv"
DADOS_TRATADOS = PASTA_DADOS / "employee_attrition.parquet"

# coloque abaixo o caminho para os arquivos de modelos de seu projeto
PASTA_MODELOS = PASTA_PROJETO / "modelos"
MODELO_FINAL = PASTA_MODELOS / "logistic_regression_rus.joblib"

# coloque abaixo outros caminhos que você julgar necessário
PASTA_RELATORIOS = PASTA_PROJETO / "relatorios"
PASTA_IMAGENS = PASTA_RELATORIOS / "imagens"
