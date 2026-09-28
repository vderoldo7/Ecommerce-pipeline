import kagglehub
import pandas as pd
import os


# ==========================================================
# 1. CARREGAMENTO DA BASE
# ==========================================================

path = kagglehub.dataset_download(
    "abbas829/ecommerce-sales-dataset"
)

file_path = os.path.join(
    path,
    "ecommerce_sales_analytics_5000.csv"
)

df = pd.read_csv(file_path)


# ==========================================================
# 2. ANÁLISE INICIAL DA BASE
# ==========================================================

print("\n--- PRIMEIRAS 5 LINHAS ---")
print(df.head())

print("\n--- COLUNAS ---")
print(df.columns.tolist())

print("\n--- TAMANHO DA BASE ---")
print(df.shape)

print("\n--- TIPOS DE DADOS ---")
print(df.dtypes)

print("\n--- VALORES NULOS ---")
print(df.isnull().sum())

print("\n--- DUPLICADOS ---")
print(df.duplicated().sum())

print("\n--- IDs DE PEDIDO DUPLICADOS ---")
print(df["order_id"].duplicated().sum())

print("\n--- ESTATÍSTICAS NUMÉRICAS ---")
print(df.describe())

print("\n--- VALORES ÚNICOS POR COLUNA ---")

for coluna in df.select_dtypes(include="object").columns:
    print(f"\n{coluna}:")
    print(df[coluna].unique())

print("\n--- QUANTIDADE DE VALORES ÚNICOS ---")
print(df.nunique())


# ==========================================================
# 3. ANÁLISE DAS DATAS
# ==========================================================

print("\n--- INTERVALO DE DATAS ---")

print("Data mínima:", df["order_date"].min())
print("Data máxima:", df["order_date"].max())


print("\n--- DISTRIBUIÇÃO POR ANO ---")

df_temp = df.copy()

df_temp["order_date"] = pd.to_datetime(
    df_temp["order_date"],
    format="%m/%d/%Y"
)

print(
    df_temp["order_date"]
    .dt.year
    .value_counts()
    .sort_index()
)


# ==========================================================
# 4. VALIDAÇÃO DOS VALORES
# ==========================================================

print("\n--- VALORES FORA DO ESPERADO ---")

print(
    "Quantidade <= 0:",
    (df["quantity"] <= 0).sum()
)

print(
    "Preço <= 0:",
    (df["unit_price"] <= 0).sum()
)

print(
    "Desconto < 0:",
    (df["discount"] < 0).sum()
)

print(
    "Desconto > 1:",
    (df["discount"] > 1).sum()
)

print(
    "Dias de entrega <= 0:",
    (df["delivery_days"] <= 0).sum()
)

print(
    "Avaliação < 1:",
    (df["customer_rating"] < 1).sum()
)

print(
    "Avaliação > 5:",
    (df["customer_rating"] > 5).sum()
)

print(
    "Receita <= 0:",
    (df["revenue"] <= 0).sum()
)


# ==========================================================
# 5. VALIDAÇÃO DA RECEITA ORIGINAL
# ==========================================================

print("\n--- VALIDAÇÃO DA RECEITA ---")

receita_calculada = (
    df["quantity"]
    * df["unit_price"]
    * (1 - df["discount"])
)

diferenca = (
    df["revenue"] - receita_calculada
).abs()

print(
    "Diferenças acima de R$ 0,01:",
    (diferenca > 0.01).sum()
)

print(
    "Maior diferença:",
    diferenca.max()
)


# ==========================================================
# 6. ANÁLISES CATEGÓRICAS
# ==========================================================

print("\n--- DISTRIBUIÇÃO DAS CATEGORIAS ---")
print(df["product_category"].value_counts())

print("\n--- DISTRIBUIÇÃO DAS REGIÕES ---")
print(df["region"].value_counts())

print("\n--- DISTRIBUIÇÃO DOS PAGAMENTOS ---")
print(df["payment_method"].value_counts())


# ==========================================================
# 7. CRIAÇÃO DA BASE TRATADA
# ==========================================================

print("\n==================================")
print("\n--- CRIAÇÃO DA BASE TRATADA ---")

df_clean = df.copy()


# Conversão da data

df_clean["order_date"] = pd.to_datetime(
    df_clean["order_date"],
    format="%m/%d/%Y"
)


# Limitação do período até 2026

df_clean = df_clean[
    df_clean["order_date"] <= "2026-12-31"
].copy()


# ==========================================================
# 8. VALIDAÇÃO DO PERÍODO TRATADO
# ==========================================================

print("\n--- PERÍODO DA BASE TRATADA ---")

print(
    "Data mínima:",
    df_clean["order_date"].min()
)

print(
    "Data máxima:",
    df_clean["order_date"].max()
)

print("\n--- TAMANHO DA BASE TRATADA ---")

print(df_clean.shape)

print("\n--- REGISTROS POR ANO ---")

print(
    df_clean["order_date"]
    .dt.year
    .value_counts()
    .sort_index()
)

print("\n--- TIPOS DE DADOS DA BASE TRATADA ---")

print(df_clean.dtypes)


# ==========================================================
# 9. VALIDAÇÃO DA BASE TRATADA
# ==========================================================

print("\n--- VALIDAÇÃO DA BASE TRATADA ---")

print(
    "Linhas duplicadas:",
    df_clean.duplicated().sum()
)

print(
    "IDs de pedido duplicados:",
    df_clean["order_id"].duplicated().sum()
)

print(
    "Valores nulos:",
    df_clean.isnull().sum().sum()
)


# ==========================================================
# 10. VALIDAÇÃO DOS VALORES DA BASE TRATADA
# ==========================================================

print("\n--- VALIDAÇÃO DOS VALORES DA BASE TRATADA ---")

print(
    "Quantidade <= 0:",
    (df_clean["quantity"] <= 0).sum()
)

print(
    "Preço <= 0:",
    (df_clean["unit_price"] <= 0).sum()
)

print(
    "Desconto < 0:",
    (df_clean["discount"] < 0).sum()
)

print(
    "Desconto > 1:",
    (df_clean["discount"] > 1).sum()
)

print(
    "Dias de entrega <= 0:",
    (df_clean["delivery_days"] <= 0).sum()
)

print(
    "Avaliação < 1:",
    (df_clean["customer_rating"] < 1).sum()
)

print(
    "Avaliação > 5:",
    (df_clean["customer_rating"] > 5).sum()
)

print(
    "Receita <= 0:",
    (df_clean["revenue"] <= 0).sum()
)


# ==========================================================
# 11. CRIAÇÃO DA RECEITA BRUTA
# ==========================================================

print("\n--- CRIANDO RECEITA BRUTA ---")

df_clean["gross_revenue"] = (
    df_clean["quantity"]
    * df_clean["unit_price"]
)

print(
    df_clean[
        [
            "quantity",
            "unit_price",
            "discount",
            "gross_revenue",
            "revenue"
        ]
    ].head()
)


# ==========================================================
# 12. VALIDAÇÃO DA RECEITA APÓS TRATAMENTO
# ==========================================================

print("\n--- VALIDAÇÃO DA RECEITA APÓS TRATAMENTO ---")

receita_calculada = (
    df_clean["quantity"]
    * df_clean["unit_price"]
    * (1 - df_clean["discount"])
)

diferenca = (
    df_clean["revenue"] - receita_calculada
).abs()

print(
    "Diferenças acima de R$ 0,01:",
    (diferenca > 0.01).sum()
)

print(
    "Maior diferença:",
    diferenca.max()
)


# ==========================================================
# 13. TRADUÇÃO DOS VALORES CATEGÓRICOS
# ==========================================================

print("\n--- TRADUZINDO VALORES CATEGÓRICOS ---")


df_clean["product_category"] = df_clean[
    "product_category"
].replace({
    "Electronics": "Eletrônicos",
    "Clothing": "Roupas",
    "Home": "Casa",
    "Beauty": "Beleza"
})


df_clean["region"] = df_clean[
    "region"
].replace({
    "North": "Norte",
    "South": "Sul",
    "East": "Leste",
    "West": "Oeste"
})


df_clean["payment_method"] = df_clean[
    "payment_method"
].replace({
    "Card": "Cartão",
    "COD": "Pagamento na entrega",
    "Wallet": "Carteira digital"
})


# ==========================================================
# 14. PADRONIZAÇÃO DOS NOMES DAS COLUNAS
# ==========================================================

print("\n--- PADRONIZANDO NOMES DAS COLUNAS ---")

df_clean = df_clean.rename(
    columns={
        "order_id": "id_pedido",
        "order_date": "data_pedido",
        "customer_id": "id_cliente",
        "product_category": "categoria_produto",
        "region": "regiao",
        "quantity": "quantidade",
        "unit_price": "preco_unitario",
        "discount": "desconto",
        "payment_method": "metodo_pagamento",
        "delivery_days": "dias_entrega",
        "customer_rating": "avaliacao_cliente",
        "revenue": "receita",
        "gross_revenue": "receita_bruta"
    }
)


# ==========================================================
# 15. VALIDAÇÃO FINAL
# ==========================================================

print("\n--- COLUNAS FINAIS ---")
print(df_clean.columns.tolist())


print("\n--- VALORES CATEGÓRICOS FINAIS ---")

print(
    "\nCategorias:"
)

print(
    df_clean["categoria_produto"].unique()
)


print(
    "\nRegiões:"
)

print(
    df_clean["regiao"].unique()
)


print(
    "\nMétodos de pagamento:"
)

print(
    df_clean["metodo_pagamento"].unique()
)


print("\n--- VALIDAÇÃO FINAL DA BASE ---")

print("Linhas:", len(df_clean))

print("Colunas:", len(df_clean.columns))

print(
    "Valores nulos:",
    df_clean.isnull().sum().sum()
)

print(
    "Linhas duplicadas:",
    df_clean.duplicated().sum()
)


print("\n--- PRIMEIRAS 5 LINHAS DA BASE FINAL ---")

print(df_clean.head())


# ==========================================================
# 16. SALVAMENTO DA BASE TRATADA
# ==========================================================

print("\n--- SALVANDO BASE TRATADA ---")

df_clean.to_csv(
    "ecommerce_clean.csv",
    index=False
)

print(
    "Arquivo ecommerce_clean.csv criado com sucesso!"
)