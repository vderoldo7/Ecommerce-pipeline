import oracledb
import pandas as pd

# ==========================================
# 1. Ler o arquivo CSV
# ==========================================

df = pd.read_csv("ecommerce_clean.csv")

print(f"CSV carregado: {len(df)} registros")


# ==========================================
# 2. Conectar ao Oracle
# ==========================================

username = ""
password = input("Digite sua senha do Oracle: ")

connection = oracledb.connect(
    user=username,
    password=password,
    dsn="oracle.fiap.com.br:1521/ORCL"
)

cursor = connection.cursor()

print("Conexão com Oracle realizada com sucesso!")


# ==========================================
# 3. Preparar o INSERT
# ==========================================

sql = """
    INSERT INTO PROJ_ECOMMERCE_VENDAS (
        id_pedido,
        data_pedido,
        id_cliente,
        categoria_produto,
        regiao,
        quantidade,
        preco_unitario,
        desconto,
        metodo_pagamento,
        dias_entrega,
        avaliacao_cliente,
        receita,
        receita_bruta
    )
    VALUES (
        :1,
        TO_DATE(:2, 'YYYY-MM-DD'),
        :3,
        :4,
        :5,
        :6,
        :7,
        :8,
        :9,
        :10,
        :11,
        :12,
        :13
    )
"""


# ==========================================
# 4. Converter os dados
# ==========================================

dados = []

for _, row in df.iterrows():
    dados.append((
        int(row["id_pedido"]),
        row["data_pedido"],
        int(row["id_cliente"]),
        row["categoria_produto"],
        row["regiao"],
        int(row["quantidade"]),
        float(row["preco_unitario"]),
        float(row["desconto"]),
        row["metodo_pagamento"],
        int(row["dias_entrega"]),
        float(row["avaliacao_cliente"]),
        float(row["receita"]),
        float(row["receita_bruta"])
    ))


# ==========================================
# 5. Inserir os dados
# ==========================================

cursor.executemany(sql, dados)

connection.commit()

print(f"{cursor.rowcount} registros inseridos com sucesso!")


# ==========================================
# 6. Fechar conexão
# ==========================================

cursor.close()
connection.close()

print("Conexão encerrada.")
