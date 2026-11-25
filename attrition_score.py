import pandas as pd
from sqlalchemy import create_engine, URL
connection_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="root",
    host="localhost",
    port=3306,
    database="customer_attrition"
)

engine = create_engine(connection_url)

df = pd.read_sql(
    "SELECT * FROM customer_attrition_dataset",
    engine
)

print("MySQL connection successful!")
print(df.head())

def calculate_risk(row):
    score = 0
    reasons = []
    balance_decline_pct = 0
    txn_decline_pct = 0

    # Balance decline: 50 points if >= 30%
    if row["account_balance_6m_ago"] > 0:
        balance_decline_pct = (
            (row["account_balance_6m_ago"] - row["current_balance"])
            / row["account_balance_6m_ago"] * 100
        )
        if balance_decline_pct >= 30:
            score += 50
            reasons.append("Balance declined by 30% or more")

    # Transaction decline: 50 points if >= 40%
    if row["transactions_6m_ago"] > 0:
        txn_decline_pct = (
            (row["transactions_6m_ago"] - row["current_transactions"])
            / row["transactions_6m_ago"] * 100
        )
        if txn_decline_pct >= 40:
            score += 50
            reasons.append("Transactions declined by 40% or more")

    # Extra rule: no balance change AND no current transactions.
    # Classify this customer as HIGH risk and NON-ACTIVATED.
    if (
        row["account_balance_6m_ago"] == row["current_balance"]
        and row["current_transactions"] == 0
    ):
        score = 100
        category = "HIGH"
        reasons.append("NON-ACTIVATED: No balance change and no transactions")
    elif score == 100:
        category = "HIGH"
    elif score == 50:
        category = "MEDIUM"
    else:
        category = "LOW"

    return pd.Series([
        round(balance_decline_pct, 2),
        round(txn_decline_pct, 2),
        score,
        category
    ])

# Calculate the risk score and explanation for every customer
df[[
    "balance_decline_pct",
    "transaction_decline_pct",
    "attrition_risk_score",
    "risk_category"
]] = df.apply(calculate_risk, axis=1)

# Retrieve medium- and high-risk customers, including NON-ACTIVATED customers
priority_customers = df[df["risk_category"].isin(["HIGH", "MEDIUM"])].sort_values(
    ["attrition_risk_score", "balance_decline_pct", "transaction_decline_pct"],
    ascending=False
)

print("\\n--- Customers requiring retention follow-up ---")
print(priority_customers[[
    "customer_id", "customer_name", "balance_decline_pct",
    "transaction_decline_pct", "attrition_risk_score", "risk_category"
    ]].to_string(index=False))

# Export prioritized customer list for Power BI / relationship managers
priority_customers.to_csv("attrition_warning_customers.csv", index=False)

