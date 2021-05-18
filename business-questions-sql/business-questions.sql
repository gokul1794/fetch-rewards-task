-- When considering total number of items purchased from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?
SELECT rewards_receipt_status,sum(purchased_item_count) FROM public.receipts
WHERE rewards_receipt_status='FINISHED' or rewards_receipt_status = 'REJECTED'
GROUP BY rewards_receipt_status;
-- Finished greater than rejected

-- When considering average spend from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?
SELECT rewards_receipt_status,avg(total_spent) as average FROM public.receipts
WHERE rewards_receipt_status='FINISHED' or rewards_receipt_status = 'REJECTED'
GROUP BY rewards_receipt_status order by average desc;
-- Finished greater than rejected

-- What are the top 5 brands by receipts scanned for most recent month?
select brand_code,count(brand_code) as cnt from public.receipt_item ri
inner join public.receipts r on r.receipt_id = ri.receipt_id
where EXTRACT(MONTH FROM r.create_date) = 1
group by brand_code order by cnt desc limit 5;
-- There are 6 records for February, the most records are in January 
-- and no records in March, April or May

-- Which brand has the most spend among users who were created within the past 6 months?
select brand_code,sum(total_spent) as total FROM public.users u 
inner join public.receipts r on r.user_id = u.user_id
inner join receipt_item on receipt_item.receipt_id = r.receipt_id
where u.created_date >  CURRENT_DATE - INTERVAL '6 months'
group by brand_code
order by total desc offset 1 limit 1;
-- The first result is null(beacause a lot of items don't have the brand captured, 
-- but excluding that Ben and Jerry's seem to be the most spent brand.