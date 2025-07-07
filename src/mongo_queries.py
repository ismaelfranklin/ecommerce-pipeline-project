import csv
import json
from pymongo import MongoClient
import os

# Função para exportar dados para CSV
def export_csv(filename, data, headers):
    os.makedirs("data/olist/insight", exist_ok=True)
    
    path = f"data/olist/insight/{filename}"
    with open(path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print(f"{filename} salvo com sucesso!")


if __name__ == "__main__":
    # Conectar ao MongoDB local
    client = MongoClient("mongodb://localhost:27017/")
    db = client["olist_ecommerce"]

    # 1. Vendas por mês
    vendas_mes = list(db.orders.aggregate([
        {"$group": {"_id": {"$substr": ["$order_date", 0, 7]}, "total_pedidos": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]))
    vendas_mes_csv = [{"mes": v["_id"], "total_pedidos": v["total_pedidos"]} for v in vendas_mes]
    export_csv("vendas_por_mes.csv", vendas_mes_csv, headers=["mes", "total_pedidos"])

    # 2. Vendas por estado
    vendas_estado = list(db.orders.aggregate([
        {"$group": {"_id": "$customer.state", "total_pedidos": {"$sum": 1}}},
        {"$sort": {"total_pedidos": -1}}
    ]))
    vendas_estado_csv = [{"estado": v["_id"], "total_pedidos": v["total_pedidos"]} for v in vendas_estado]
    export_csv("vendas_por_estado.csv", vendas_estado_csv, headers=["estado", "total_pedidos"])

    # 3. Total de vendas
    total_vendas = list(db.orders.aggregate([
        {"$group": {"_id": None, "total_vendas": {"$sum": "$payment.value"}}}
    ]))
    export_csv("vendas_totais.csv", total_vendas, ["_id", "total_vendas"])

    # 4. Frete médio por pedido
    frete_medio = list(db.orders.aggregate([
        {"$unwind": "$items"},
        {"$group": {"_id": "$order_id", "frete_total": {"$sum": "$items.freight_value"}}},
        {"$group": {"_id": None, "frete_medio": {"$avg": "$frete_total"}}}
    ]))
    export_csv("frete_medio.csv", frete_medio, ["_id", "frete_medio"])

    # 5. Top 5 produtos mais vendidos
    mais_vendidos = list(db.orders.aggregate([
        {"$unwind": "$items"},
        {"$group": {"_id": "$items.product_id", "total_vendido": {"$sum": 1}}},
        {"$sort": {"total_vendido": -1}},
        {"$limit": 5}
    ]))
    export_csv("produtos_mais_vendidos.csv", mais_vendidos, ["_id", "total_vendido"])

    # 6. Formas de pagamento mais utilizadas
    formas_pagamento = list(db.orders.aggregate([
        {"$group": {"_id": "$payment.type", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}}
    ]))
    export_csv("formas_pagamento.csv", formas_pagamento, ["_id", "total"])

    # 7. Média de avaliação
    avaliacoes = list(db.orders.aggregate([
        {"$group": {"_id": None, "media_avaliacao": {"$avg": "$review.score"}}}
    ]))
    export_csv("avaliacoes.csv", avaliacoes, ["_id", "media_avaliacao"])
