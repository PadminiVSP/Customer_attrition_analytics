# Customer Attrition Early-Warning Analysis

## Project Overview
This project focuses on identifying banking customers who may be showing early signs of reduced engagement by analysing changes in their account balances and transaction activities over a six-month period.

Using SQL and Python (Pandas), a simple rule-based scoring model is developed to identify customers who may require retention follow-up.

## Technologies Used
- **SQL (MySQL):** Data retrieval and customer analysis
- **Python:** Rule-based risk scoring
- **Pandas:** Data manipulation and analysis

## Business Rules
- Balance decline of 30% or more: 50 points.
- Transaction decline of 40% or more: 50 points.
- Both conditions triggered: HIGH risk (100 points).
- One condition triggered: MEDIUM risk (50 points).
- No warning indicators: LOW risk (0 points).
- Unchanged account balance with zero current transactions: HIGH risk – NON-ACTIVATED.

## Key Outcomes
- Identifies customers showing declining banking activity.
- Highlights non-activated customers.
- Classifies customers based on attrition risk.
- Generates a prioritised customer list for potential retention follow-up.

## Objective
To demonstrate how banking domain knowledge, SQL and Python can be combined to develop a simple, explainable customer attrition early-warning solution and support data-driven banking decisions.

*Note: This is an educational rule-based prototype developed using sample data, not a validated predictive model.*
