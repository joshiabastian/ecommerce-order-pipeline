-- datamart: top fraud users
-- identifikasi user yang paling sering melakukan transaksi fraud

with fraud_orders as (
    select
        user_id,
        user_name,
        gender,
        age_group,
        count(*)                as total_fraud_orders,
        sum(amount)             as total_fraud_amount,
        count(distinct country) as unique_countries,
        min(created_date)       as first_fraud_date,
        max(created_date)       as last_fraud_date
    from {{ ref('fact_orders') }}
    where status = 'frauds'
    group by user_id, user_name, gender, age_group
)