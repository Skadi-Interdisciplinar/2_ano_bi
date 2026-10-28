-- Dashboard de Chamados
-- Execute cada consulta separadamente no Databricks SQL e associe o resultado a um visual.

-- 1. Cards: total, abertos, finalizados e tempo medio de resolucao.
SELECT
  COUNT(*) AS total_chamados,
  SUM(CASE WHEN esta_aberto THEN 1 ELSE 0 END) AS chamados_abertos,
  SUM(CASE WHEN esta_finalizado THEN 1 ELSE 0 END) AS chamados_finalizados,
  AVG(CASE WHEN esta_finalizado THEN tempo_resolucao_minutos END) AS tempo_medio_resolucao_minutos
FROM gold_chamados;

-- 2. Barras: chamados por status.
SELECT status, COUNT(*) AS quantidade
FROM gold_chamados
GROUP BY status
ORDER BY quantidade DESC;

-- 3. Barras: chamados por categoria.
SELECT categoria, COUNT(*) AS quantidade
FROM gold_chamados
GROUP BY categoria
ORDER BY quantidade DESC;

-- 4. Barras: chamados por responsavel.
SELECT
  COALESCE(CAST(cod_usuario_responsavel AS STRING), 'NAO ATRIBUIDO') AS responsavel,
  COUNT(*) AS quantidade
FROM gold_chamados
GROUP BY COALESCE(CAST(cod_usuario_responsavel AS STRING), 'NAO ATRIBUIDO')
ORDER BY quantidade DESC;

-- 5. Linha: aberturas por dia.
SELECT
  CAST(data_hora_abertura AS DATE) AS dia,
  COUNT(*) AS chamados_abertos
FROM gold_chamados
GROUP BY CAST(data_hora_abertura AS DATE)
ORDER BY dia;

-- 6. Linha: finalizacoes por dia.
SELECT
  CAST(data_hora_encerramento AS DATE) AS dia,
  COUNT(*) AS chamados_finalizados
FROM gold_chamados
WHERE esta_finalizado
GROUP BY CAST(data_hora_encerramento AS DATE)
ORDER BY dia;

-- 7. Histograma e boxplot: distribuicao do tempo de resolucao.
SELECT
  chamado_id,
  categoria,
  data_hora_abertura,
  tempo_resolucao_minutos
FROM gold_chamados
WHERE esta_finalizado
  AND tempo_resolucao_minutos IS NOT NULL;
