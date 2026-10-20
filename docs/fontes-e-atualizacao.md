# Fontes e atualização

## Fontes PostgreSQL

- `tb_usuario`: total e distribuição de usuários por nível de acesso.
- `tb_solicitacao_suporte`: chamados, status, categoria, responsável e datas.
- `tb_controle_rpa`: última execução bem-sucedida da carga RPA selecionada.

## Camadas

- Bronze: leitura dos campos necessários da fonte operacional.
- Silver: tipos corrigidos, valores padronizados, duplicidades removidas e validações.
- Gold: bases finais sem CPF, senha, e-mail ou descrição do chamado.

## Atualização

Na primeira etapa, Bronze, Silver e Gold são executados manualmente nessa ordem. Depois de validados, os notebooks serão adaptados para um Pipeline Databricks e poderão ser acionados por Job manual ou agendado.
