
CREATE TABLE store (
  store_id INT PRIMARY KEY,
  store_name TEXT,
  store_state TEXT,
  store_type TEXT
);

CREATE TABLE sales_fact_1997 (
  store_id INT,
  store_sales NUMERIC,
  store_cost NUMERIC,
  unit_sales INT
);

INSERT INTO store VALUES
(1,'LA Supermarket','CA','Supermarket'),
(2,'SF Supermarket','CA','Supermarket'),
(3,'NY Market','NY','Market');

INSERT INTO sales_fact_1997 VALUES
(1,10000,7000,120),
(2,15000,9000,180),
(3,8000,5000,90);
