# Pipeline BI do app

O job `Skadi Gestor e Operador` executa Bronze, Silver e as Gold do gestor e do funcionário nessa ordem. A configuração do job está em `app/pipeline/job_gestor_e_operador.yaml`; os caminhos dos notebooks são relativos aos arquivos do repositório para evitar dependência da pasta de um usuário específico.

As regras de SLA compartilhadas pelas duas Gold ficam em `app/notebooks/sla_rules.py`. A regra calcula o percentual consumido, o estado do prazo e a etapa prevista (Operador, Gestor, Admin ou vencido); ela não altera o responsável nem envia notificações.

## Validar e executar o bundle no Databricks

Execute os comandos a partir da raiz do repositório, onde está `databricks.yml`:

```powershell
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle run -t dev Skadi_Gestor_e_Operador
```

O CLI usa o perfil Databricks autenticado na sua máquina. O alvo `dev` instala os recursos no diretório do usuário autenticado, definido automaticamente pelo bundle. Não coloque tokens, senhas ou URLs de autenticação nos arquivos do projeto.
