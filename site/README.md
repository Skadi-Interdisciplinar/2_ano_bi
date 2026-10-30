# Dashboards do Site

Esta área prepara os dados dos dashboards de **Chamados** e **Superadmin**.

## Dashboard de Chamados

- Total de chamados, chamados abertos e finalizados.
- Chamados por status, categoria e responsável.
- Evolução diária de aberturas e finalizações.
- Tempo médio, histograma e boxplot de resolução dos chamados atendidos.

## Dashboard de Superadmin

- Total de usuários e distribuição por nível de acesso.
- Chamados abertos e tempo médio de resolução.
- Última execução bem-sucedida da carga RPA configurada.

## Bases finais

- `gold_chamados`
- `gold_superadmin_usuarios`
- `gold_superadmin_rpa`

Os notebooks em `notebooks/` preparam as camadas Bronze, Silver e Gold dessas bases. A pasta `pipeline/` receberá a execução automatizada das mesmas transformações.

O notebook `notebooks/dashboard_site.ipynb` gera os painéis visuais finais de Chamados e Superadmin com cards, barras, linhas, histograma e boxplot.
