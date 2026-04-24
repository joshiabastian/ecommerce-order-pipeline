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
),
 
all_orders as (
    select
        user_id,
        count(*) as total_orders
    from {{ ref('fact_orders') }}
    group by user_id
)
 
select
    f.user_id,
    f.user_name,
    f.gender,
    f.age_group,
    f.total_fraud_orders,
    a.total_orders,
    round(f.total_fraud_orders / a.total_orders * 100, 2) as fraud_rate_pct,
    f.total_fraud_amount,
    f.unique_countries,
    f.first_fraud_date,
    f.last_fraud_date
 
from fraud_orders f
left join all_orders a on f.user_id = a.user_id
order by f.total_fraud_orders desc