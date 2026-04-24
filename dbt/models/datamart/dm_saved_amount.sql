-- datamart: saved amount
-- menghitung jumlah uang yang berhasil diselamatkan berkat fraud detection

with daily as (
    select
        date(created_date)      as order_date,
        status,
        count(*)                as total_orders,
        sum(amount)             as total_amount
    from {{ ref('fact_orders') }}
    group by date(created_date), status
),

pivoted as (
    select
        order_date,
        sum(case when status = 'genuine' then total_orders else 0 end) as genuine_orders,
        sum(case when status = 'frauds'  then total_orders else 0 end) as fraud_orders,
        sum(case when status = 'genuine' then total_amount else 0 end) as genuine_amount,
        sum(case when status = 'frauds'  then total_amount else 0 end) as fraud_amount,
        sum(total_orders)                                               as total_orders,
        sum(total_amount)                                               as total_amount
    from daily
    group by order_date
)

select
    order_date,
    genuine_orders,
    fraud_orders,
    total_orders,
    genuine_amount,
    fraud_amount                                                        as saved_amount,
    total_amount,
    round(fraud_orders / total_orders * 100, 2)                        as fraud_rate_pct,
    round(fraud_amount / total_amount * 100, 2)                        as saved_amount_pct

from pivoted
order by order_date desc