-- Dashboard de Superadmin
-- Execute cada consulta separadamente no Databricks SQL e associe o resultado a um visual.

-- 1. Cards: total de usuarios, chamados abertos, tempo medio e ultima carga RPA.
SELECT
  MAX(total_usuarios) AS total_usuarios,
  (SELECT COUNT(*) FROM gold_chamados WHERE esta_aberto) AS chamados_abertos,
  (SELECT AVG(tempo_resolucao_minutos)
   FROM gold_chamados
   WHERE esta_finalizado AND tempo_resolucao_minutos IS NOT NULL) AS tempo_medio_resolucao_minutos,
  (SELECT MAX(ultima_execucao_sucesso) FROM gold_superadmin_rpa) AS ultima_execucao_rpa
FROM gold_superadmin_usuarios;

-- 2. Barras: usuarios por nivel de acesso.
SELECT nivel_acesso, quantidade_usuarios
FROM gold_superadmin_usuarios
ORDER BY nivel_acesso;

-- 3. Barras: chamados por status.
SELECT status, COUNT(*) AS quantidade
FROM gold_chamados
GROUP BY status
ORDER BY quantidade DESC;

-- 4. Linha: evolucao diaria de chamados abertos e finalizados.
SELECT
  dia,
  SUM(chamados_abertos) AS chamados_abertos,
  SUM(chamados_finalizados) AS chamados_finalizados
FROM (
  SELECT CAST(data_hora_abertura AS DATE) AS dia, 1 AS chamados_abertos, 0 AS chamados_finalizados
  FROM gold_chamados
  UNION ALL
  SELECT CAST(data_hora_encerramento AS DATE) AS dia, 0 AS chamados_abertos, 1 AS chamados_finalizados
  FROM gold_chamados
  WHERE esta_finalizado
) eventos
GROUP BY dia
ORDER BY dia;

-- 5. Histograma e boxplot: tempo de resolucao dos chamados atendidos.
SELECT
  chamado_id,
  categoria,
  tempo_resolucao_minutos
FROM gold_chamados
WHERE esta_finalizado
  AND tempo_resolucao_minutos IS NOT NULL;
