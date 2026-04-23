-- preparation layer: users
-- standarisasi nomor telepon ke format +62XXXXXXXXX

with raw as (
    select * from {{ source('yosia_finpro', 'users') }}
),

cleaned as (
    select
        user_id,
        name,
        email,

        -- bersihkan nomor telepon:
        -- 1. hapus semua karakter non-digit
        -- 2. kalau mulai '0' → ganti jadi '62'
        -- 3. kalau sudah mulai '62' → pertahankan
        -- 4. tambahkan prefix '+'
        '+' || case
            when regexp_replace(phone_number, r'[^0-9]', '') like '0%'
                then '62' || substr(regexp_replace(phone_number, r'[^0-9]', ''), 2)
            when regexp_replace(phone_number, r'[^0-9]', '') like '62%'
                then regexp_replace(phone_number, r'[^0-9]', '')
            else regexp_replace(phone_number, r'[^0-9]', '')
        end as phone_number,

        address,
        city,
        age,
        gender,
        is_active,
        created_date

    from raw
)

select * from cleaned