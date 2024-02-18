
--Calculate total sales amount per customer.
SELECT customer_id, SUM(quantity * price) AS total_sales_amount
FROM [dbo].[orders_details]
GROUP BY customer_id
order by total_sales_amount


--Determine the average order quantity per product.
SELECT product_id, AVG(quantity) AS average_order_quantity
FROM [dbo].[orders_details]
GROUP BY product_id
order by product_id

--TOP Customer with top-selling Products
WITH RankedData AS (
    SELECT
        customer_id,
        product_id,
        SUM(quantity) AS total_quantity,
        RANK() OVER (PARTITION BY customer_id ORDER BY SUM(quantity) DESC) AS customer_rank,
        RANK() OVER (PARTITION BY product_id ORDER BY SUM(quantity) DESC) AS product_rank
    FROM [dbo].[orders_details]
    GROUP BY customer_id, product_id
)
SELECT
    customer_id AS top_customer_id,
    product_id AS top_product_id,
    total_quantity
FROM RankedData
WHERE customer_rank = 1 AND product_rank = 1
order by top_customer_id asc,top_product_id asc,total_quantity

--Identify the top-selling products or customers.
--Identify the top-selling products:
SELECT product_id, SUM(quantity) AS total_sold
FROM [dbo].[orders_details]
GROUP BY product_id
ORDER BY total_sold DESC

--Identify the top customers:
SELECT customer_id, SUM(quantity) AS total_purchased
FROM [dbo].[orders_details]
GROUP BY customer_id
ORDER BY total_purchased DESC

--Analyze sales trends over time  monthly
SELECT
    YEAR(order_date) AS order_year,
    MONTH(order_date) AS order_month,
    SUM(quantity * price) AS monthly_sales
FROM [dbo].[orders_details]
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY order_year, order_month

--Analyze sales trends over time quarterly sales).
SELECT
    YEAR(order_date) AS order_year,
    CEILING(MONTH(order_date) / 3.0) AS order_quarter,
    SUM(quantity * price) AS quarterly_sales
FROM [dbo].[orders_details]
GROUP BY YEAR(order_date), CEILING(MONTH(order_date) / 3.0)
ORDER BY order_year, order_quarter


-- Average Sales Based on Weather Condition
with weather_data as(
SELECt oc.*,wd.weather_description,wd.weather_main,wd.city 
FROM [dbo].[orders_details] oc
LEFT JOIN users_details ud
on oc.customer_id=ud.customer_id
LEFT JOIN location_fictious_address fa
on ud.city=fa.city
LEFT JOIN weather_details wd
on fa.city=wd.city
)

SELECT weather_description as  Weather_Description,AVG(quantity * price) as AverageSales 
FROM weather_data
Group by weather_description


-- Average Sales Based on Weather Condition with temperature wise
with f_data as(
SELECt oc.*,wd.weather_description,wd.weather_main,wd.city,wd.temp
FROM [dbo].[orders_details] oc
LEFT JOIN users_details ud
on oc.customer_id=ud.customer_id
LEFT JOIN location_fictious_address fa
on ud.city=fa.city
LEFT JOIN weather_details wd
on fa.city=wd.city
)

-- Average Sales Based on Weather Condition
SELECT weather_description as  Weather_Description,AVG(quantity * price) as AverageSales,AVG(temp) AS AVG_Temperature 
FROM f_data
Group by weather_description
