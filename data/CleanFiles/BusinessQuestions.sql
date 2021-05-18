SELECT rewards_receipt_status,sum(purchased_item_count) FROM public.receipts
WHERE rewards_receipt_status='FINISHED' or rewards_receipt_status = 'REJECTED'
GROUP BY rewards_receipt_status;

SELECT rewards_receipt_status,avg(total_spent) as average FROM public.receipts
WHERE rewards_receipt_status='FINISHED' or rewards_receipt_status = 'REJECTED'
GROUP BY rewards_receipt_status order by average desc;

select count(receipt_id) as count_scanned from public.receipt_item ri
inner join public.brands br on br.barcode = ri.barcode;

select brand_code,count(brand_code) as cnt from public.receipt_item ri
inner join public.receipts r on r.receipt_id = ri.receipt_id
where EXTRACT(MONTH FROM r.create_date) = 1
group by brand_code order by cnt desc limit 5;

select brand_code,sum(total_spent) as total FROM public.users u 
inner join public.receipts r on r.user_id = u.user_id
inner join receipt_item on receipt_item.receipt_id = r.receipt_id
where u.created_date >  CURRENT_DATE - INTERVAL '6 months'
group by brand_code
order by total desc offset 1;
order by u.created_date desc

select brand_code,count(brand_code) as cnt, max(total_spent),  from public.receipt_item ri
inner join public.receipts r on r.receipt_id = ri.receipt_id 
where EXTRACT(MONTH FROM r.create_date) = 1
group by brand_code order by cnt desc limit 5;
