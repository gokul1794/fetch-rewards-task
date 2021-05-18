-- Quality Checks
-- There are 117 users in Receipts table, that are not present in the user's table at all.
Select count (distinct user_id) num_user_id from receipts
where user_id not in
(Select user_id from users);

-- The Brands table also had duplicated rows with the same brand_id which I think is supposed to be a primary key.
-- I dropped these duplicate keys while processing the data in python.