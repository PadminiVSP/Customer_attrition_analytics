-- Simple MySQL attrition warning view using balance and transaction decline only.
CREATE DATABASE IF NOT EXISTS attrition_analytics;
USE attrition_analytics;

DROP TABLE IF EXISTS customer_attrition_data;
CREATE TABLE customer_attrition_data (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100),
    account_balance_6m_ago DECIMAL(15,2),
    current_balance DECIMAL(15,2),
    transactions_6m_ago INT,
    current_transactions INT,
    digital_logins_6m_ago INT,
    current_digital_logins INT,
    days_since_last_transaction INT,
    complaints_last_6m INT,
    fd_maturity_days INT NULL,
    fd_renewed TINYINT,
    salary_credit_active TINYINT,
    loan_closed_recently TINYINT,
    other_products_count INT
);

-- Import the CSV into customer_attrition_data using MySQL Workbench's
-- Table Data Import Wizard after running the table creation above.

CREATE OR REPLACE VIEW vw_customer_attrition_warning AS
SELECT
    customer_id,
    customer_name,
    account_balance_6m_ago,
    current_balance,
    transactions_6m_ago,
    current_transactions,
    ROUND((account_balance_6m_ago - current_balance)
          / NULLIF(account_balance_6m_ago, 0) * 100, 2) AS balance_decline_pct,
    ROUND((transactions_6m_ago - current_transactions)
          / NULLIF(transactions_6m_ago, 0) * 100, 2) AS transaction_decline_pct,
    (CASE WHEN account_balance_6m_ago > 0
              AND current_balance <= account_balance_6m_ago * 0.70
         THEN 50 ELSE 0 END
     + CASE WHEN transactions_6m_ago > 0
              AND current_transactions <= transactions_6m_ago * 0.60
         THEN 50 ELSE 0 END) AS attrition_risk_score,
    CASE
        WHEN account_balance_6m_ago > 0
             AND current_balance <= account_balance_6m_ago * 0.70
             AND transactions_6m_ago > 0
             AND current_transactions <= transactions_6m_ago * 0.60
        THEN 'HIGH'
        WHEN (account_balance_6m_ago > 0
              AND current_balance <= account_balance_6m_ago * 0.70)
          OR (transactions_6m_ago > 0
              AND current_transactions <= transactions_6m_ago * 0.60)
        THEN 'MEDIUM'
        ELSE 'LOW'
    END AS risk_category
FROM customer_attrition_data;

-- Retrieve customers requiring retention follow-up:
-- SELECT * FROM vw_customer_attrition_warning
-- WHERE risk_category IN ('HIGH', 'MEDIUM')
-- ORDER BY attrition_risk_score DESC;
