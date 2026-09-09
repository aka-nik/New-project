# Olist Source Profile

This profile describes the original Olist files before any cleaning or transformation.

## Table inventory

| File | Rows | Columns | Role |
|---|---:|---:|---|
| `olist_orders_dataset.csv` | 99,441 | 8 | One row per order |
| `olist_order_items_dataset.csv` | 112,650 | 7 | One row per product line within an order |
| `olist_customers_dataset.csv` | 99,441 | 5 | Customer and location identifiers |
| `olist_products_dataset.csv` | 32,951 | 9 | Product attributes |
| `olist_order_payments_dataset.csv` | 103,886 | 5 | Payment records |
| `olist_order_reviews_dataset.csv` | 99,224 | 7 | Customer reviews |
| `olist_sellers_dataset.csv` | 3,095 | 4 | Seller and location identifiers |
| `olist_geolocation_dataset.csv` | 1,000,163 | 5 | ZIP-code geographic coordinates |
| `product_category_name_translation.csv` | 71 | 2 | Portuguese-to-English category names |

## Initial findings

- `order_id` is unique in the orders table.
- `order_id` repeats in order items because one order can contain multiple products. This is an expected one-to-many relationship.
- Orders have missing timestamps: 160 missing approval dates, 1,783 missing carrier-delivery dates, and 2,965 missing customer-delivery dates.
- Products have 610 missing category and descriptive attribute values. Two products have missing physical dimensions and weight.
- Customer and product identifiers are unique in their own tables.

## First pipeline slice

The first implementation will use orders, order items, customers, and products. Payments, reviews, sellers, geography, and category translation will be added after this slice is understood and tested.

## Useful interview language

> The orders table has order-level grain, while order items has order-line grain. I keep those grains separate so aggregations do not multiply revenue or item counts during joins.
