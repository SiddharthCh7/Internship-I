use urbandb;
SELECT * FROM services;

SELECT COUNT(package_id),segmentation_type_id FROM services GROUP BY segmentation_type_id HAVING COUNT(package_id) = 1;

SELECT service_id, price FROM services HAVING price > 399;

SELECT price, COUNT(*) as c FROM services GROUP BY price HAVING price > 399 AND price < 1799;

-- Group by
SELECT package_id, COUNT(package_id) FROM services GROUP BY package_id;

-- Order by
SELECT service_id, price FROM services ORDER BY price;

-- Having
SELECT service_id, package_id, price FROM services GROUP BY service_id, package_id HAVING price > 399 and price < 2000;
SELECT service_id, service_name, service_duration FROM services GROUP BY service_id HAVING service_duration > 45 and service_duration < 2000;
SELECT service_name, service_duration, price FROM services GROUP BY service_id HAVING service_duration > 45 and price < 2000;

-- Join
SELECT major_category.mc_id, subcategory.subcategory_name FROM major_category JOIN subcategory ON subcategory.mc_id = major_category.mc_id;

-- Distinct
SELECT DISTINCT package_id FROM services;
SELECT DISTINCT price FROM services HAVING price BETWEEN 399 AND 2000;
SELECT DISTINCT segmentation_type_id, AVG(price) FROM services GROUP BY segmentation_type_id;

-- LIKE
SELECT * FROM services WHERE service_name LIKE "%Hair%";
SELECT * FROM package WHERE package_name LIKE "%Botox%";
SELECT * FROM services WHERE service_name LIKE "%spa%";

-- CASE
SELECT service_name, price, CASE WHEN price >399 THEN 'pass' ELSE 'fail' END AS 'remark' FROM services;
-- IF
SELECT service_name, price, IF(price > 399,'pass','fail') AS 'remark' FROM services;

-- GROUPCONCAT
SELECT package_id, service_name, GROUP_CONCAT(service_id) as "services" FROM services group by service_name,service_id;

-- LENGTH
SELECT service_id, service_name, LENGTH(service_name) as "length" FROM services;