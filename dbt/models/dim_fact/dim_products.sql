-- dim & fact layer: dim_products

with prep as (
    select * from {{ ref('prep_products') }}
)

select
    product_id,
    product_name,
    category,
    brand,
    price,
    stock,
    is_available,
    created_date,
    price_segment,
    stock_status

from prep