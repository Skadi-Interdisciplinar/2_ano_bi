# Dashboards do Site no Databricks

As consultas deste diretório usam exclusivamente as tabelas Gold produzidas pelos notebooks:

- `gold_chamados`
- `gold_superadmin_usuarios`
- `gold_superadmin_rpa`

O notebook `../notebooks/dashboard_site.ipynb` gera os painéis finais em Python com Matplotlib. Ele deve ser executado em um compute Python, como Serverless CPU ou GPU. Ele possui widgets interativos para status, categoria, responsável, período e nível de acesso. O notebook `../notebooks/visualizacoes_site.ipynb` permanece como versão exploratória das visualizações.

## Dashboard de Chamados

Use `chamados.sql` para criar:

- cards de total, abertos, finalizados e tempo médio;
- barras por status, categoria e responsável;
- linhas de aberturas e finalizações por dia;
- histograma e boxplot do tempo de resolução dos chamados `ATENDIDO`.

Filtros aplicáveis: período de abertura/encerramento, status, categoria e responsável.

## Dashboard de Superadmin

Use `superadmin.sql` para criar:

- cards de usuários, chamados abertos, tempo médio e última carga RPA;
- barras por nível de acesso e status de chamado;
- linha de evolução diária de aberturas e finalizações;
- histograma e boxplot do tempo de resolução.

Filtro aplicável: período, status e nível de acesso quando o visual utilizar usuários.

## Montagem no Databricks

1. Abra o SQL Editor e selecione o mesmo catálogo/schema em que as tabelas Gold foram gravadas.
2. Crie uma query para cada bloco separado por comentário no arquivo correspondente.
3. Execute cada query e escolha o tipo de visual indicado.
4. Adicione os visuais ao dashboard correspondente.
5. Configure os filtros interativos usando as colunas disponíveis no resultado da query.

Não há mapa, pois este escopo não possui KPI geográfico definido.
