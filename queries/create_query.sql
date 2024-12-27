-- tabela customers
CREATE TABLE `nexus-443823.nxscase2024.customers_file3` (
  customer_id STRING,
  customer_name STRING,
  customer_email STRING
);


-- transactions 1
CREATE TABLE `nexus-443823.nxscase2024.transactions_file1` (
  transaction_id STRING,
  customer_id STRING,
  transaction_date DATE,
  transaction_amount FLOAT64,
  transaction_status STRING
);


-- transaction 2 
CREATE TABLE `nexus-443823.nxscase2024.transactions_file2` (
  transaction_id STRING,
  transaction_type STRING,
  qtty FLOAT64,
  price FLOAT64
);
