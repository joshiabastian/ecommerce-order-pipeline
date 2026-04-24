-- datamart: user segments
-- segmentasi user berdasarkan frekuensi dan nilai transaksi (RFM sederhana)

with user_stats as (
    select
        user_id,
        user_name,
        gender,
        age_group,
        count(*)                                            as total_orders,
        countif(status = 'frauds')                         as total_frauds,
        sum(case when status = 'genuine' then amount end)  as total_genuine_spend,
        sum(amount)                                        as total_spend,
        round(avg(case when status = 'genuine' then amount end), 2) as avg_order_value,
        max(created_date)                                  as last_order_date,
        count(distinct product_category)                   as unique_categories,
        count(distinct payment_method)                     as unique_payment_methods

    from {{ ref('fact_orders') }}
    group by user_id, user_name, gender, age_group
),

segmented as (
    select
        *,
        -- segmentasi berdasarkan frekuensi dan spend genuine
        case
            when total_frauds > 0                               then 'Fraud Risk'
            when total_orders >= 10 and total_genuine_spend >= 1000000 then 'High Value'
            when total_orders >= 5                              then 'Regular'
            when total_orders >= 2                              then 'Occasional'
            else                                                     'One-time'
        end as user_segment

    from user_stats
)

select * from segmented
order by total_genuine_spend desc