use amazon;
create table products
(
	pid int(3) primary key,
    pname varchar(50) not null,
    price int(10) not null,
    stock int(5),
    location varchar(30) check(location in ('Mumbai','Delhi'))
);
create table customer
(
	cid int(3) primary key,
    cname varchar(30) not null,
    age int(3),
    addr varchar(50)
);
create table orders
(
	oid int(3) primary key,
    cid int(3),
    pid int(3),
    amt int(10) not null,
    foreign key(cid) references customer(cid),
    foreign key(pid) references products(pid)
);
create table payment
(
	pay_id int(3) primary key,
    oid int(3),
    amount int(10) not null,
    mode varchar(30) check(mode in('upi','credit','debit')),
    status varchar(30),
    foreign key(oid) references orders(oid)
);

CREATE TABLE employee(
eid INT(4) PRIMARY KEY,
ename VARCHAR(40) NOT NULL,
phone_no INT(10) NOT NULL,
department VARCHAR(40) NOT NULL,
manager_id INT(4)
);
insert into products values(1,'HP Laptop',50000,15,'Mumbai');
insert into products values(2,'Realme Mobile',20000,30,'Delhi');
insert into products values(3,'Boat earpods',3000,50,'Delhi');
insert into products values(4,'Levono Laptop',40000,15,'Mumbai');
insert into products values(5,'Charger',1000,0,'Mumbai');
insert into products values(6, 'Mac Book', 78000, 6, 'Delhi');
insert into products values(7, 'JBL speaker', 6000, 2, 'Delhi');

#Inserting values into customer table
insert into customer values(101,'Ravi',30,'fdslfjl');
insert into customer values(102,'Rahul',25,'fdslfjl');
insert into customer values(103,'Simran',32,'fdslfjl');
insert into customer values(104,'Purvesh',28,'fdslfjl');
insert into customer values(105,'Sanjana',22,'fdslfjl');

insert into orders values(10001,102,3,2700);
insert into orders values(10002,104,2,18000);
insert into orders values(10003,105,5,900);
insert into orders values(10004,101,1,46000);

insert into payment values(1,10001,2700,'upi','completed');
insert into payment values(2,10002,18000,'credit','completed');
insert into payment values(3,10003,900,'debit','in process');

#Inserting into employee table
INSERT INTO employee VALUES (401, "Rohan", 364832549, "Analysis", 404);
INSERT INTO employee VALUES (402, "Rahul", 782654123, "Delivery", 406);
INSERT INTO employee VALUES (403, "Shyam", 856471235, "Delivery", 402);
INSERT INTO employee VALUES (404, "Neha", 724863287, "Sales", 402);
INSERT INTO employee VALUES (405, "Sanjana", 125478954, "HR", 404);
INSERT INTO employee VALUES (406, "Sanjay", 956478535, "Tech",null);

use amazon;
SELECT customer.cid, cname, orders.oid FROM orders 
INNER JOIN customer ON orders.cid = customer.cid;

SELECT o.oid, c.cname, o.amt
FROM orders o
JOIN customer c ON o.cid = c.cid;

SELECT o.oid, c.cname, p.pname, o.amt
FROM orders o
JOIN customer c ON o.cid = c.cid
JOIN products p ON o.pid = p.pid;

SELECT p.pay_id, o.oid, p.amount, p.mode, p.status
FROM payment p
JOIN orders o ON p.oid = o.oid;

SELECT p.pay_id, o.oid, c.cname, p.amount, p.mode, p.status
FROM payment p
JOIN orders o ON p.oid = o.oid
JOIN customer c ON o.cid = c.cid;

SELECT o.oid, o.amt, p.pay_id, p.amount AS payment_amount
FROM orders o
LEFT JOIN payment p ON o.oid = p.oid
WHERE p.pay_id IS NULL;

SELECT p.pname, SUM(o.amt) AS total_sales
FROM products p
JOIN orders o ON p.pid = o.pid
GROUP BY p.pname;

SELECT e1.ename AS Employee, e2.ename AS Manager
FROM employee e1
JOIN employee e2 ON e1.manager_id = e2.eid;

SELECT o.oid, p.pname, p.location, o.amt
FROM orders o
JOIN products p ON o.pid = p.pid
WHERE p.location = 'Mumbai';

SELECT c.cname, o.oid, p.pay_id, p.amount, p.status
FROM customer c
JOIN orders o ON c.cid = o.cid
JOIN payment p ON o.oid = p.oid
WHERE p.status = 'Completed';

select cname from customer 
where cid=(select cid   
from orders 
order by amt 
desc limit 1);

select cname from customer where cid = (select cid from orders order by amt);

-- Finding the costliest product
select pname from products where price=(select price from products order by price desc limit 1);
select pname from products where price=(select max(price) from products);

-- Selecting customers from Delhi who have placed orders
select cname from customer where cid IN (select cid from orders where pid IN (select pid from products where location="Delhi"));

-- Selecting customers whose order amount exceeded the average order amount
select cname from customer where exists(select 1 from orders where orders.cid=customer.cid group by orders.cid having avg(orders.amt) >(select avg(amt) from orders));

SELECT cname
FROM customer c
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.cid = c.cid
    GROUP BY o.cid
    HAVING AVG(o.amt) > (
        SELECT AVG(amt)
        FROM orders
    )
);
