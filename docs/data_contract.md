# Initial Data Contract

This contract describes the first four source tables. The quality checks and later ingestion code will treat these rules as expectations.

## Orders

- File: `olist_orders_dataset.csv`
- Grain: one row per order
- Primary key: `order_id`
- Required reference: `customer_id` must exist in customers
- Nullable timestamps: delivery-related timestamps may be empty for orders that have not reached that stage

## Order items

- File: `olist_order_items_dataset.csv`
- Grain: one row per product line within an order
- Composite business identity: `order_id` + `order_item_id`
- Foreign keys: `order_id` must exist in orders; `product_id` must exist in products
- `price` and `freight_value` are monetary source fields

## Customers

- File: `olist_customers_dataset.csv`
- Grain: one row per customer-order location record
- Primary key: `customer_id`
- `customer_unique_id` identifies the person across potentially multiple order records

## Products

- File: `olist_products_dataset.csv`
- Grain: one row per product
- Primary key: `product_id`
- `product_category_name` and physical attributes may be missing and must be reported, not silently invented

## Relationship rules

| Child table | Child column | Parent table | Parent column |
|---|---|---|---|
| orders | `customer_id` | customers | `customer_id` |
| order items | `order_id` | orders | `order_id` |
| order items | `product_id` | products | `product_id` |

## Baseline result

The original source currently has zero orphan rows for all three relationships. This is the baseline against which later deliberately messy test data will be compared.
