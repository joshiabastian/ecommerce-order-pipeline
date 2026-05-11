-- dim & fact layer: fact_orders
-- join orders dengan dim_users dan dim_products

with orders as (
    select * from {{ ref('prep_orders') }}
),

users as (
    select user_id, name, city as user_city, gender, age_group
    from {{ ref('dim_users') }}
),

products as (
    select product_id, product_name, category, brand, price_segment
    from {{ ref('dim_products') }}
)

SELECT
    o.order_id,
    o.user_id,
    u.name                  AS user_name,
    u.gender                AS user_gender,
    u.age_group,
    o.product_id,
    p.product_name,
    p.category              AS product_category,
    p.brand,
    p.price_segment,
    o.quantity,
    o.amount,
    o.country,
    o.city                  AS order_city,
    o.payment_method,
    o.device,
    o.created_date,
    o.updated_date,
    o.status,
    o.order_hour,
    o.is_rawan,
    o.processing_time_ms

FROM orders o
LEFT JOIN users    u ON o.user_id    = u.user_id
LEFT JOIN products p ON o.product_id = p.product_id