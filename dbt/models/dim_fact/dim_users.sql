-- dim & fact layer: dim_users
-- tambah age_group untuk segmentasi umur

with prep as (
    select * from {{ ref('prep_users') }}
)

select
    user_id,
    name,
    email,
    phone_number,
    address,
    city,
    age,
    gender,
    is_active,
    created_date,

    -- segmentasi umur
    case
        when age between 15 and 20 then 'Gen Z (15-20)'
        when age between 21 and 27 then 'Young Adult (21-27)'
        when age between 28 and 35 then 'Adult (28-35)'
        else                            'Mature (36-45)'
    end as age_group

from prep