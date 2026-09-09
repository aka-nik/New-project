# Architecture Decisions

## ADR-001: Choose the Olist Brazilian E-Commerce Dataset

**Status:** Accepted

**Decision:** Use the public Brazilian E-Commerce dataset from Olist as the project's source domain.

**Why:**

- It contains related tables for orders, customers, products, sellers, payments, reviews, and geography.
- It is large enough to demonstrate joins, deduplication, data quality checks, and dimensional modelling.
- It is still small enough to run locally on a laptop.
- The domain is easy to explain in an interview: an order moves from purchase to delivery and review.

**Initial pipeline slice:**

1. Start with orders, order items, customers, and products.
2. Add payments, reviews, sellers, and geography after the first slice works.
3. Create deliberately messy copies of the source files for quality testing.
4. Keep the original source data unchanged as the raw baseline.

**Out of scope for the first step:** Airflow, Docker, MinIO, dbt, and LLM calls. They will be added only after the data can be inspected and understood.

**Interview explanation:**

> I chose Olist because its related entities let me demonstrate a realistic e-commerce pipeline and a star schema, while its size keeps local development inexpensive and reproducible.
