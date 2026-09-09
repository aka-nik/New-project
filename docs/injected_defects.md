# Injected Defect Manifest

This document records the deliberate defects used to test the first version of the ETL quality checks. The clean baseline remains in the original source files under `data/source/`.

## Orders table

| Defect | Example | Expected detection | Notes |
|---|---|---|---|
| Duplicate order keys | The same `order_id` appears twice | Duplicate-key check | This simulates a re-ingest or a bad upstream feed |
| Missing critical values | Empty `order_status` or `order_purchase_timestamp` | Null/missing-value check | The row is still readable but should be quarantined |
| Whitespace in identifiers | `customer_id` or `order_id` with leading/trailing spaces | Trim-and-normalise validation | These values should be treated as equivalent after cleaning |

## Products table

| Defect | Example | Expected detection | Notes |
|---|---|---|---|
| Category spelling drift | `Electronics`, `electronics`, `ELECTRONIC`, `Elec.`, `Consumer Electronics` | Canonicalisation / categorical audit | The rule is that variants should map to one canonical value |
| Missing category labels | Blank `product_category_name` | Null/missing-value check | This should be reported without invention |

## Intended quality outcomes

The deterministic checks should catch:

- Duplicate keys in the orders file
- Missing values in critical columns
- Non-normalised textual identifiers with stray whitespace
- Inconsistent category names that should be mapped to a single canonical label

The generator in `scripts/make_messy.py` is the source of truth for creating the test dataset used in unit tests and early data-quality validation.
