# 📊 Dashboard Pedidos E-Commerce

Este projeto é um pipeline completo de dados que utiliza Python para realizar o processo de ETL, armazena e analisa dados com BigQuery, e visualiza as informações com o Looker Studio.

---

## 🧱 Estrutura do Projeto

```
ecommerce-pipeline-project/
│
├── data/olist/               # Dados brutos utilizados
├── dashboard/                # Configurações ou imagens do dashboard
├── notebooks/                # Explorações e validações em Jupyter Notebooks
├── src/                      # Scripts principais
│   ├── etl.py                # Script ETL para tratar dados CSV
│   ├── mongo_queries.py      # Consultas MongoDB (alternativas de análise)
│   └── to_mongo.py           # Upload para MongoDB (corrigido nome)
│
├── requirements.txt          # Bibliotecas necessárias
└── README.md                 # Este arquivo
```

---

## ⚙️ Tecnologias utilizadas

- 🦍 **Python** para extração e transformação dos dados
- 📆 **Pandas** para manipulação tabular
- 🎃 **MongoDB** como banco de dados NoSQL alternativo
- ☁️ **Google BigQuery** para armazenamento e análise escalável
- 📊 **Google Looker Studio** para criação de dashboards interativos

---

## ⚙️ Scripts principais

| Script             | Descrição                                                      |
| ------------------ | -------------------------------------------------------------- |
| `etl.py`           | Lê arquivos CSV, trata dados nulos, renomeia colunas e exporta |
| `mongo_queries.py` | Contém consultas MongoDB para análises rápidas                 |
| `to_mongo.py`      | Realiza upload dos dados tratados para o MongoDB               |

---

## 📈 Métricas e Visualizações (Looker Studio)

- Valor total de vendas
- Valor médio do frete
- Média de avaliações
- Total de pedidos por mês (série temporal)
- Total de pedidos por estado (gráfico de barras)
- Produtos mais vendidos
- Formas de pagamento (gráfico pizza)

🧱 Com filtros interativos por estado e data.

📸 **Preview do Dashboard:**

https://lookerstudio.google.com/s/l4OrUL3cGBI





---

## 🔁 Pipeline ETL

1. Extração dos dados CSV (`data/olist`)
2. Transformação com Pandas (`src/etl.py`)
3. Armazenamento em:
   - MongoDB para consultas rápidas
   - BigQuery para análise e visualização
4. Visualização com Looker Studio

---

## 🧪 Como executar

1. Crie o ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute o script ETL:

```bash
python src/etl.py
```

---

## 📂 Fonte dos Dados

Este projeto utiliza os dados públicos do Olist disponíveis no Kaggle:\
🔗 [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

---

## ✍️ Autor

Desenvolvido por **Ismael Franklin (Frank)**\
📧 [ismaelfranklin@gmail.com](mailto\:ismaelfranklin@gmail.com)\
💼 [LinkedIn](https://www.linkedin.com/in/ismaelfranklin/)

---

> Projeto com fins educacionais para prática de Engenharia de Dados e Visualização.


## Screenshots

![App Screenshot](https://github.com/ismaelfranklin/ecommerce-pipeline-project/blob/main/dashboard/Screenshot%202025-07-06%20at%2021.41.49.png)


