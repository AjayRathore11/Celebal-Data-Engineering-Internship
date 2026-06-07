use week_3;

select * from superstore_raw
limit 20;

create table customers(
	CustomerID varchar(50) ,
    CustomerName varchar(50),
    Segment varchar(30)
);
drop table customers;
Insert into customers (CustomerID,CustomerName,Segment)
select distinct `Customer ID`, `Customer Name`,`Segment`
from superstore_raw;


select * from customers
limit 5;

create table products(
	ProductID varchar(50),
    category varchar(50),
    SubCategory varchar(50),
    ProductName varchar(255)
    );
drop table products;
insert into products (ProductID, Category, SubCategory, ProductName)
select distinct `Product ID`, `Category`, `Sub-Category`, `Product Name`
from superstore_raw;


create table orders (
    RowID int,
    OrderID varchar(50),
    OrderDate varchar(20),
    ShipDate varchar(20),
    ShipMode varchar(50),
    CustomerID varchar(50),
    ProductID varchar(50),
    Country varchar(50),
    City varchar(100),
    State varchar(100),
    PostalCode varchar(20),
    Region varchar(50),
    Sales Decimal(10, 4),
    Quantity int,
    Discount Decimal(4, 2),
    Profit decimal(10, 4)
);


insert into orders (
    RowID, OrderID, OrderDate, ShipDate, ShipMode, CustomerID, ProductID, 
    Country, City, State, PostalCode, Region, Sales, Quantity, Discount, Profit
)
select distinct 
    `Row ID`, `Order ID`, `Order Date`, `Ship Date`, `Ship Mode`, `Customer ID`, `Product ID`, 
    `Country`, `City`, `State`, `Postal Code`, `Region`, `Sales`, `Quantity`, `Discount`, `Profit`
from superstore_raw;


-- Step 2   -----------------------------

-- 1.Find all orders where sales are greater than the average sales. (Subquery)  
select OrderID, CustomerID,OrderDate,Sales
from orders
where Sales > (
    select AVG(Sales) 
    from orders
);

-- 2.Find the highest sales order for each customer. (Subquery)  
select OrderID, CustomerID,OrderDate,Sales
from orders
where (CustomerID, Sales) IN (
    select CustomerID, MAX(Sales)
    from orders
    group by CustomerID
);


-- 3. Calculate total sales for each customer. (CTE)  
with CustomerTotalSales as (
    select CustomerID, sum(Sales) as TotalSales
    from orders
    group by CustomerID
)
-- Now we select from the CTE we just created, and join the customers table to get their names!
select c.CustomerName,cts.CustomerID, cts.TotalSales
from CustomerTotalSales cts
join customers c on cts.CustomerID = c.CustomerID
order by cts.TotalSales desc;

-- 4.Find customers whose total sales are above average. (CTE + Subquery)
with CustomerTotalSales AS (
    select CustomerID, SUM(Sales) as TotalSales
    from orders
    group by CustomerID
)
select c.CustomerName,cts.CustomerID, cts.TotalSales
from CustomerTotalSales cts
join customers c on cts.CustomerID = c.CustomerID
where cts.TotalSales > (
    select avg(TotalSales) 
    from CustomerTotalSales
)
order by  cts.TotalSales Desc;

-- 5.Rank all customers based on total sales. (Window Function)  
with CustomerTotals as (
    select CustomerID, SUM(Sales) as TotalSales
    from orders
    group by CustomerID
)
select c.CustomerName, ct.TotalSales,
    Rank() over (order by ct.TotalSales desc) as SalesRank
from CustomerTotals as ct
join customers as c on ct.CustomerID = c.CustomerID;

-- 6.Assign row numbers to each order within a customer. (Window Function + PARTITION BY)  
select CustomerID, OrderID, OrderDate, 
    ROW_NUMBER() over (PARTITION BY CustomerID order by OrderDate) as OrderNumber
from orders;

-- 7.Display top 3 customers based on total sales. (Window Function)  
with CustomerRankings as (
    select CustomerID,SUM(Sales) as TotalSales,
        RANK() over (order by SUM(Sales) desc) as SalesRank
    from orders
    group by CustomerID
)
select c.CustomerName,cr.TotalSales,cr.SalesRank
from CustomerRankings as cr
join customers as c on cr.CustomerID = c.CustomerID
where cr.SalesRank <= 3;



-- Step 3 Final combined Query 

with CustomerTotals as (
    select CustomerID, SUM(Sales) as TotalSales
    from orders
    group by  CustomerID
)
select c.CustomerName, ct.TotalSales,
    RANK() over (order by ct.TotalSales Desc) as SalesRank
from CustomerTotals ct
join customers c ON ct.CustomerID = c.CustomerID;



-- Mini project : Customer sales Insights

-- 1. Top 5 customers
select c.CustomerName, SUM(o.Sales) as TotalSales
from orders as o
join customers as c on o.CustomerID = c.CustomerID
group by c.CustomerID, c.CustomerName
order by TotalSales DESC
LIMIT 5;

-- 2. Bottom 5 customers
select c.CustomerName, SUM(o.Sales) as TotalSales
from orders as o
join customers as c on o.CustomerID = c.CustomerID
group by c.CustomerID, c.CustomerName
order by TotalSales asc
LIMIT 5;

-- 3. which customer made only one order
select c.CustomerName, 
    count(distinct o.OrderID) as NumberOfOrders
from orders as o
join customers as c on o.CustomerID = c.CustomerID
group by c.CustomerID, c.CustomerName
having count(distinct o.OrderID) = 1;

-- 4. which customer have above avg sales
WITH CustomerSales AS (
    select CustomerID, SUM(Sales) as TotalSales
    from orders
    group by CustomerID
)
select c.CustomerName, cs.TotalSales
from CustomerSales cs
join customers as c on cs.CustomerID = c.CustomerID
where cs.TotalSales > (
    select AVG(TotalSales) 
    from CustomerSales
)
order by cs.TotalSales desc;

-- 5. Highest order vales per customer

with OrderValues as (
    select CustomerID, OrderID, SUM(Sales) AS OrderTotal
    from orders
    group by CustomerID, OrderID
)
select c.CustomerName, MAX(ov.OrderTotal) as HighestOrderValue
from  OrderValues as ov
join customers as c on ov.CustomerID = c.CustomerID
group by c.CustomerID, c.CustomerName
order by HighestOrderValue desc ;




