-- datamart: sales by category
-- analisis penjualan genuine per kategori dan brand

select
    product_category,
    brand,
    price_segment,
    count(*)                                as total_orders,
    sum(quantity)                           as total_quantity,
    sum(amount)                             as total_revenue,
    round(avg(amount), 2)                   as avg_order_value,
    round(avg(quantity), 2)                 as avg_quantity,
    count(distinct user_id)                 as unique_buyers,
    countif(status = 'frauds')              as fraud_orders,
    round(
        countif(status = 'frauds') / count(*) * 100, 2
    )                                       as fraud_rate_pct

from {{ ref('fact_orders') }}
group by product_category, brand, price_segment
order by total_revenue desc