# SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# PACKAGE_DIR="$(dirname "$SCRIPT_DIR")"
# Diretório base do Airflow
# export AIRFLOW_HOME="$PACKAGE_DIR"

AIRFLOW_VERSION=2.8.1

# Extraia a versão do Python que tem instalada no ambinete. Se estiver utilizando uma versão do Python não suportada pelo Airflow, será necessário definir manualmente.
# A partir do Airflow 2.7.0, o Airflow suporta Python 3.8, 3.9, 3.10 e 3.11
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"

# Por exemplo, isto instalaria a versão 2.8.1 com python 3.8: https://raw.githubusercontent.com/apache/airflow/constraints-2.8.1/constraints-3.8.txt
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

# Embora tenha havido sucesso com o uso de outras ferramentas como poetry ou pip-tools, elas não compartilham o mesmo fluxo de trabalho que o pip - especialmente quando se trata de gerenciamento de restrições vs. requisitos. A instalação via Poetry ou pip-tools não é suportada atualmente.

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
