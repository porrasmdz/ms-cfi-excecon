#General Client Info
#################################################
#CLIENT INFO AND WAREHOUSE INFO (THIS COULD BE A NORMAL VIEW, VALIDATE DIFF)
#################################################
CREATE VIEW general_client_info
AS
SELECT cmy.ruc, cmy.codename, cmy.name AS company, 
	wh.name AS warehouse, wh.country, wh.state, wh.city, wh.address, cc.id AS cyclic_count_id
FROM company AS cmy
JOIN cyclic_count AS cc ON cc.company_id = cmy.id
LEFT JOIN warehouse AS wh ON cmy.id = wh.company_id;

SELECT * FROM general_client_info;
--------
SELECT cmy.ruc, cmy.codename, cmy.name AS company, 
	wh.name AS warehouse, wh.country, wh.state, wh.city, wh.address 
FROM company AS cmy
JOIN cyclic_count AS cc ON cc.company_id = cmy.id
LEFT JOIN warehouse AS wh ON cmy.id = wh.company_id
WHERE cc.id = 'c4118b7e-e683-4772-8fc7-62e1ce1d000d';

#####################################################
#COUNT_RESPONSIBLES / ASIGNEES (THIS COULD BE A NORMAL VIEW, VALIDATE DIFF)
#####################################################
(HAVE TO ADD USER_ID to cycliccount and Supervisor_ID)

#####################################################
#WAREHOUSE CONTROL DATA 
#####################################################
CREATE VIEW wh_control_data
AS
SELECT cpt.cyclic_count_id, COUNT(sr.registry_units) AS sys_registries, SUM(sr.registry_units) AS sys_unit, SUM(sr.registry_cost) AS total_usd_system
FROM ccount_product_table AS cpt 
LEFT OUTER JOIN product AS pr ON pr.id = cpt.product_id
LEFT OUTER JOIN count_registry AS sr ON sr.cyclic_count_id = cpt.cyclic_count_id AND sr.product_id = cpt.product_id AND sr.registry_type = 'system'
GROUP BY cpt.cyclic_count_id;

SELECT * FROM wh_control_data;
----------
SELECT COUNT(sr.registry_units) AS sys_registries, SUM(sr.registry_units) AS sys_unit, SUM(sr.registry_cost) AS total_usd_system
FROM ccount_product_table AS cpt 
LEFT OUTER JOIN product AS pr ON pr.id = cpt.product_id
LEFT OUTER JOIN count_registry AS sr ON sr.cyclic_count_id = cpt.cyclic_count_id AND sr.product_id = cpt.product_id AND sr.registry_type = 'system'
WHERE cpt.cyclic_count_id = 'c4118b7e-e683-4772-8fc7-62e1ce1d000d';

#############################################
#OBTAINED RESULTS 
#############################################
(QUERY cyclic_count_history VIEW AND FILTER WITH PANDAS 
TO GET BETTER FINE GRAINED RESULTS UNIVERSE, REF, EXCEEDING, LACKING ETC...)

##############################################
#CYCLIC_COUNT_HISTORY
##############################################
#GOtta backtrack to get all counts history

CREATE MATERIALIZED VIEW IF NOT EXISTS cyclic_count_history
AS
SELECT cpt.cyclic_count_id, wh.name AS warehouse, pr.id AS product_id,
	pr.code, pr.name, pr.sku, pr.unit_cost, 
	mu.name AS measure_unit, pc.name AS category,
	sr.registry_units AS system_units, phr.registry_units AS physical_units, phr.difference_units AS diff_units,
	sr.registry_cost AS total_usd_system, phr.registry_cost AS total_usd_physical, phr.difference_cost AS total_usd_diff
FROM ccount_product_table AS cpt 
LEFT OUTER JOIN product AS pr ON pr.id = cpt.product_id
LEFT OUTER JOIN count_registry AS sr ON sr.cyclic_count_id = cpt.cyclic_count_id AND sr.product_id = cpt.product_id AND sr.registry_type = 'system'
LEFT OUTER JOIN count_registry AS phr ON phr.cyclic_count_id = cpt.cyclic_count_id AND phr.product_id = cpt.product_id AND phr.registry_type = 'physical'
LEFT OUTER JOIN measure_unit AS mu ON mu.id = pr.measure_unit_id
LEFT OUTER JOIN product_category AS pc ON pc.id = pr.category_id
LEFT OUTER JOIN warehouse_ccount_table AS whct ON whct.cyclic_count_id = cpt.cyclic_count_id 
LEFT OUTER JOIN warehouse AS wh ON wh.id = whct.warehouse_id
WITH NO DATA;

SELECT * FROM cyclic_count_history;
REFRESH MATERIALIZED VIEW [CONCURRENTLY] cyclic_count_history;
--------------------

SELECT cpt.cyclic_count_id, wh.name AS warehouse,
	pr.code, pr.name, pr.sku, pr.unit_cost, 
	mu.name AS measure_unit, pc.name AS category,
	sr.registry_units AS system_units, phr.registry_units AS physical_units, phr.difference_units AS diff_units,
	sr.registry_cost AS total_usd_system, phr.registry_cost AS total_usd_physical, phr.difference_cost AS total_usd_diff
FROM ccount_product_table AS cpt 
LEFT OUTER JOIN product AS pr ON pr.id = cpt.product_id
LEFT OUTER JOIN count_registry AS sr ON sr.cyclic_count_id = cpt.cyclic_count_id AND sr.product_id = cpt.product_id AND sr.registry_type = 'system'
LEFT OUTER JOIN count_registry AS phr ON phr.cyclic_count_id = cpt.cyclic_count_id AND phr.product_id = cpt.product_id AND phr.registry_type = 'physical'
LEFT OUTER JOIN measure_unit AS mu ON mu.id = pr.measure_unit_id
LEFT OUTER JOIN product_category AS pc ON pc.id = pr.category_id
LEFT OUTER JOIN warehouse_ccount_table AS whct ON whct.cyclic_count_id = cpt.cyclic_count_id 
LEFT OUTER JOIN warehouse AS wh ON wh.id = whct.warehouse_id
WHERE cpt.cyclic_count_id = 'c4118b7e-e683-4772-8fc7-62e1ce1d000d';