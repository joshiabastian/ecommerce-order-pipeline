-- preparation layer: orders
-- tambah kolom turunan untuk analisis fraud dan performa

with raw as (
    select * from {{ source('yosia_finpro', 'orders') }}
),

cleaned as (
    select
        order_id,
        user_id,
        product_id,
        quantity,
        amount,
        country,
        city,
        payment_method,
        device,
        created_date,
        updated_date,
        status,

        -- jam order dibuat (WIB)
        extract(hour from created_date) as order_hour,

        -- flag jam rawan (00:00 - 03:59)
        case
            when extract(hour from created_date) between 0 and 3 then true
            else false
        end as is_rawan,

        -- selisih waktu producer → consumer dalam milidetik
        timestamp_diff(updated_date, created_date, millisecond) as processing_time_ms

    from raw
)

select * from cleaned