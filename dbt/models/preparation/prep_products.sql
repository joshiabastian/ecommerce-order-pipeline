-- preparation layer: products
-- tambah price_segment dan stock_status

with raw as (
    select * from {{ source('yosia_finpro', 'products') }}
),

cleaned as (
    select
        product_id,
        product_name,
        category,
        brand,
        price,
        stock,
        is_available,
        created_date,

        -- segmentasi harga
        case
            when price < 100000  then 'Budget'
            when price < 500000  then 'Mid-range'
            else                      'Premium'
        end as price_segment,

        -- status stok
        case
            when stock = 0       then 'Out of Stock'
            when stock <= 50     then 'Low Stock'
            else                      'Available'
        end as stock_status

    from raw
)

select * from cleaned