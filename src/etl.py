import pandas as pd
import numpy as np
from collections import defaultdict
import json

# Função para ler um arquivo CSV e retornar um DataFrame
def ler_csv(filepath, sep=",") -> pd.DataFrame: 
    return pd.read_csv(filepath, sep=sep)

# Função para preencher valores nulos em uma coluna específica de um DataFrame
def preenchend_valores_nulos(df: pd.DataFrame, coluna: str, valor: str = "Sem informação") -> pd.DataFrame:
    df[coluna] = df[coluna].fillna(valor)
    return df

# Função para realizar o merge dos principais DataFrames do projeto
def merge_dataframes(orders, order_items, payments, reviews, customers):
    df = pd.merge(orders, order_items, on="order_id", how="left")
    df = pd.merge(df, payments, on="order_id", how="left")
    df = pd.merge(df, reviews, on="order_id", how="left")
    df = pd.merge(df, customers, on="customer_id", how="left")
    return df

# Função para agrupar os pedidos em formato de dicionário estruturado (útil para exportação JSON)
def group_orders(df):
    from collections import defaultdict
    orders_dict = defaultdict(lambda: {
        "order_id": None,
        "customer": {},
        "items": [],
        "payment": {},
        "review": {},
        "status": None,
        "order_date": None
    })

    # Itera sobre cada linha do DataFrame e constrói a estrutura de pedidos
    for _, row in df.iterrows():
        order = orders_dict[row['order_id']]
        order["order_id"] = row["order_id"]
        order["status"] = row["order_status"]
        order["order_date"] = row["order_purchase_timestamp"]

        order["customer"] = {
            "customer_id": row["customer_id"],
            "city": row["customer_city"],
            "state": row["customer_state"]
        }

        order["items"].append({
            "product_id": row["product_id"] if pd.notnull(row["product_id"]) else "desconhecido",
            "seller_id": row["seller_id"],
            "price": float(row["price"]) if not pd.isnull(row["price"]) else 0.0,
            "freight_value": float(row["freight_value"]) if not pd.isnull(row["freight_value"]) else 0.0
        })

        order["payment"] = {
            "type": row["payment_type"] if pd.notnull(row["payment_type"]) else "not_defined",
            "installments": int(row["payment_installments"]) if not pd.isnull(row["payment_installments"]) else 0,
            "value": float(row["payment_value"]) if not pd.isnull(row["payment_value"]) else 0.0
        }

        order["review"] = {
            "score": int(row["review_score"]) if not pd.isnull(row["review_score"]) else None,
            "comment_title": row["review_comment_title"] if pd.notnull(row["review_comment_title"]) else "",
            "comment_message": row["review_comment_message"] if pd.notnull(row["review_comment_message"]) else ""
        }

    return list(orders_dict.values())

# Bloco principal de execução
if __name__ == "__main__":    
    # Carrega os dados dos arquivos CSV
    orders = ler_csv("/Users/ismael/Documents/Projects-Data_Engineering/Nosql/ecomerce-pipeline-project/data/olist/olist_orders_dataset.csv")
    order_items = ler_csv("/Users/ismael/Documents/Projects-Data_Engineering/Nosql/ecomerce-pipeline-project/data/olist/olist_order_items_dataset.csv")
    customers = ler_csv("/Users/ismael/Documents/Projects-Data_Engineering/Nosql/ecomerce-pipeline-project/data/olist/olist_customers_dataset.csv")
    payments = ler_csv("/Users/ismael/Documents/Projects-Data_Engineering/Nosql/ecomerce-pipeline-project/data/olist/olist_order_payments_dataset.csv")
    reviews = ler_csv("/Users/ismael/Documents/Projects-Data_Engineering/Nosql/ecomerce-pipeline-project/data/olist/olist_order_reviews_dataset.csv")

    # Lista de DataFrames e nomes para referência
    dfs = [orders, order_items, customers, payments, reviews]
    df_names = ["orders", "order_items", "customers", "payments", "reviews"]

    # Preenche todos os valores nulos de todos os DataFrames com "sem informação"
    for i, (name, df) in enumerate(zip(df_names, dfs)):
        df = df.fillna("sem informação")
        dfs[i] = df
        print(f"DataFrame {name} null values after filling: {df.isnull().sum().sum()}")
        print("-" * 50)

    # Mostra as colunas do DataFrame de pedidos
    print("Colunas do DataFrame 'orders':", orders.columns.tolist())

    # Realiza o merge dos DataFrames principais
    merged_df = merge_dataframes(orders, order_items, payments, reviews, customers)

    print("Merged DataFrame:")
    print(merged_df.head()) 

    # Agrupa os pedidos em formato estruturado
    orders_json = group_orders(merged_df)
    print(f"Total de pedidos agrupados: {len(orders_json)}")
    # Exibe um exemplo de pedido agrupado em formato JSON
    print(json.dumps(orders_json[0], indent=2, ensure_ascii=False))

    # Salva o resultado em um arquivo JSON
    with open("data/olist/json/orders.json", "w", encoding="utf-8") as f:
        json.dump(orders_json, f, indent=2, ensure_ascii=False) 
    print("Arquivo JSON salvo com sucesso!")


