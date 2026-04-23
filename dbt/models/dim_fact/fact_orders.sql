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

select
    o.order_id,
    o.user_id,
    u.name                  as user_name,
    u.gender                as user_gender,
    u.age_group,
    o.product_id,
    p.product_name,
    p.category              as product_category,
    p.brand,
    p.price_segment,
    o.quantity,
    o.amount,
    o.country,
    o.city                  as order_city,
    o.payment_method,
    o.device,
    o.created_date,
    o.updated_date,
    o.status,
    o.order_hour,
    o.is_rawan,
    o.processing_time_ms

from orders o
left join users    u on o.user_id    = u.user_id
left join products p on o.product_id = p.product_id