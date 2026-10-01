# FINRA Industry Regulatory Analytics

### End-to-End Regulatory Data Analytics Project | 2011–2021

An end-to-end data analytics project using **FINRA public API data**, **Python**, **PostgreSQL**, **SQL**, and **Power BI** to analyze historical industry registration trends.

---

## Dashboard Preview

![FINRA Industry Regulatory Analytics Dashboard](docs/finra_powerbi_dashboard.png)

---

## Project Overview

The **FINRA Industry Regulatory Analytics** project analyzes historical industry registration data from **2011 to 2021**.

The project focuses on identifying trends and changes across five reported registration categories:

- All FINRA-Registered Broker-Dealer Firms
- Broker-Dealer Firms - Only
- Dual Broker-Dealer and Investment Advisers
- Investment Adviser Firms-Only
- Securities Industry Registered Firms

The project demonstrates a complete analytics workflow from API data extraction through business intelligence reporting.

---

## Business Objective

The objective of this project is to analyze historical changes in FINRA industry registration categories and answer key business questions around:

- Broker-dealer trends
- Investment adviser trends
- Registration category changes
- Year-over-year movements
- Long-term growth and decline
- CAGR
- Category comparisons
- Trend consistency
- Volatility
- Correlation between category trends
- Changes in reported registration mix

---

# Business Questions

The project addresses the following questions:

1. How did FINRA-registered broker-dealer firms change between 2011 and 2021?
2. What was the annual YoY change?
3. Which registration categories increased or decreased?
4. Which category experienced the largest percentage change?
5. How did broker-dealer firms compare with Investment Adviser Firms-Only?
6. What were the CAGR values for the major categories?
7. Were category trends consistent throughout the period?
8. How did the reported registration mix change?
9. What were the largest annual movements?
10. What statistical relationships existed between the major category trends?

---

# Technology Stack

| Area | Technology |
|---|---|
| Data Source | FINRA Public API |
| Authentication | OAuth 2.0 |
| Programming | Python |
| Data Analysis | pandas, NumPy |
| Visualization | Matplotlib |
| Database | PostgreSQL |
| Query Language | SQL |
| Business Intelligence | Power BI |
| Development Environment | Anaconda / Windows |

---

# End-to-End Workflow

```text
FINRA Public API
       │
       ▼
OAuth 2.0 Authentication
       │
       ▼
Python API Extraction
       │
       ▼
Raw JSON / CSV
       │
       ▼
Data Profiling
       │
       ▼
Data Cleaning & Validation
       │
       ▼
Processed Analytical Dataset
       │
       ├───────────────┐
       ▼               ▼
   Python EDA      PostgreSQL
       │               │
       ▼               ▼
 Visualizations     SQL Analysis
       │               │
       └───────┬───────┘
               ▼
           Power BI
               │
               ▼
       Business Insights# finra-industry-regulatory-analytics
