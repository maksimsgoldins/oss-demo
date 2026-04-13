# OSS Backend Render Starter v3.1

Patch v3.1 includes:
- `OrderSubAimItem` now returns `id`, `code`, `name`
- `/api/order-aims` returns sub-aim IDs so frontend can save service mappings correctly
- attribute involvement validation supports free-text default values when attribute has no configured possible values
- attribute delete validation retained
- attribute propagation retained
