Fluxo de Pipeline usando GCP (Dataflow & BigQuery)

📂 Estrutura do Projeto

nexus/
arquivos/          # Pasta para arquivos CSV locais
config/            # Configurações, incluindo chave de serviço
log/               # Arquivos de log gerados
service/           # Funções auxiliares (e.g., upload para GCS)
venv/              # Ambiente virtual (não incluído no Git)
pipeline.py        # Código principal do pipeline (Apache Beam)
app.py             # Script para simular o envio de arquivos para GCS
requirements.txt   # Dependências do projeto

🚀 Funcionalidades
1. **Simulação de Produtor**:
   - Um script em Python (`app.py`) simula o envio de arquivos CSV para o Cloud Storage.
2. **Pipeline de Processamento**:
   - Processa os dados utilizando Apache Beam e o Dataflow.   - Verifica, limpa e transforma os arquivos CSV em três tabelas diferentes no BigQuery.
3. **Conexão ao Power BI**:
   - Os dados processados no BigQuery são conectados ao Power BI para criar relatórios visuais.
🛠️ Passos de Configuração
### 1. **Pré-requisitos**
- **Crie os recursos no GCP**:
  - Projeto no GCP
  - Bucket no Cloud Storage (com subpastas: `templates`, `temp`, `csv_files`)
  - Dataset no BigQuery
- **Configure a mesma região para todos os recursos** (e.g., `us-west1`).
### 2. **Habilite APIs Necessárias**
- Ative as seguintes APIs no GCP:
  - Cloud Storage
  - Dataflow
  - BigQuery
  - BigQuery Storage
### 3. **Crie uma Conta de Serviço**
- Gere uma chave de serviço em formato `.json` e salve na pasta `config/`.
### 4. **Instale Dependências**
- Crie e ative um ambiente virtual:
  ```bash
  python -m venv venv
  source venv/bin/activate # ou venv/Scripts/activate no Windows
  ```
- Instale as dependências:
  ```bash
  pip install -r requirements.txt
  ```
📄 Descrição do Pipeline
1. **Leitura de Arquivos CSV**:
- Os arquivos no GCS são lidos conforme padrões definidos, como:
  - `gs://csv_files/customer*.csv`
  - `gs://csv_files/transactions_file1*.csv`
  - `gs://csv_files/transactions_file2*.csv`
2. **Transformação e Validação**:
- Classes de parsing verificam:
  - Datas válidas
  - Valores não nulos
  - Tipos de dados corretos
- Campos são convertidos e padronizados.
3. **Escrita no BigQuery**:
- Os dados tratados são salvos em tabelas BigQuery:
  - `customers_file3`
  - `transactions_file1`
  - `transactions_file2`
4. **Execução no Dataflow**:
- O pipeline é executado localmente para testes e no Dataflow para produção.

  
🗂️ Esquemas das Tabelas (BigQuery)
customers_file3

CREATE TABLE `.customers_file3` (
  customer_id STRING,
  customer_name STRING,
  customer_email STRING
);

transactions_file1

CREATE TABLE `.transactions_file1` (
  transaction_id STRING,
  customer_id STRING,
  transaction_date DATE,
  transaction_amount FLOAT64,
  transaction_status STRING
);

transactions_file2

CREATE TABLE `.transactions_file2` (
  transaction_id STRING,
  transaction_type STRING,
  qtty FLOAT64,
  price FLOAT64
);

📊 Integração com Power BI
Após o processamento dos dados no BigQuery, conecte o Power BI:
- Escolha o método **Importar Dados** para maior desempenho.
- Crie relatórios visuais com base nas tabelas do BigQuery.
🧑‍💻 Autor
- **Vinicius Farineli Freire**
Criado em **08/12/2024**
