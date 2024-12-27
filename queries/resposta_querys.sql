-- Qual o total de transações aprovadas por mês?
SELECT
  EXTRACT(YEAR FROM transaction_date) AS ano,
  EXTRACT(MONTH FROM transaction_date) AS mes,
  COUNT(*) AS total_transacoes_aprovadas
FROM `nexus-443823.nxscase2024.transactions_file1`
WHERE transaction_status = 'approved'
GROUP BY ano, mes
ORDER BY ano, mes;

-- Qual cliente teve o maior volume de transações aprovadas nos últimos 3 meses?
WITH max_data AS (
  SELECT MAX(transaction_date) AS last_date
  FROM `nexus-443823.nxscase2024.transactions_file1`
),
ultimos_3_meses AS (
  SELECT t1.customer_id, t1.transaction_id
  FROM `nexus-443823.nxscase2024.transactions_file1` t1
  CROSS JOIN max_data
  WHERE t1.transaction_status = 'approved'
    AND t1.transaction_date >= DATE_SUB(last_date, INTERVAL 3 MONTH)
)
SELECT customer_id, COUNT(*) AS qtd_transacoes_aprovadas
FROM ultimos_3_meses
GROUP BY customer_id
ORDER BY qtd_transacoes_aprovadas DESC
LIMIT 1;

-- Qual a média de transações rejeitadas por mês no último ano?
WITH max_data AS (
  SELECT MAX(transaction_date) AS last_date
  FROM `nexus-443823.nxscase2024.transactions_file1`
),
rejeitadas_ultimo_ano AS (
  SELECT
    EXTRACT(YEAR FROM transaction_date) AS ano,
    EXTRACT(MONTH FROM transaction_date) AS mes,
    COUNT(*) AS total_rejeitadas_no_mes
  FROM `nexus-443823.nxscase2024.transactions_file1`, max_data
  WHERE transaction_status = 'rejected'
    AND transaction_date >= DATE_SUB(last_date, INTERVAL 1 YEAR)
  GROUP BY ano, mes
)
SELECT AVG(total_rejeitadas_no_mes) AS media_rejeitadas_mes_ultimo_ano
FROM rejeitadas_ultimo_ano;


-- Qual o preço médio do estoque do ativo em questão
SELECT
  EXTRACT(YEAR FROM t1.transaction_date) AS ano,
  EXTRACT(MONTH FROM t1.transaction_date) AS mes,
  AVG(t2.price) AS preco_medio
FROM `nexus-443823.nxscase2024.transactions_file1` t1
JOIN `nexus-443823.nxscase2024.transactions_file2` t2
  ON t1.transaction_id = t2.transaction_id
GROUP BY ano, mes
ORDER BY ano, mes;
