# Azure Deployment Guidelines

Este documento contém instruções detalhadas para implantar o projeto AutoIta no Azure App Service.

## Pré-requisitos

- Conta Azure com permissões para criar recursos
- Azure CLI instalado
- Git instalado

## Variáveis de Ambiente Necessárias

Configure as seguintes variáveis de ambiente no portal do Azure App Service:

```
DJANGO_SETTINGS_MODULE=PI_2.settings_production
DJANGO_SECRET_KEY=<sua-chave-secreta>
WEBSITE_HTTPLOGGING_RETENTION_DAYS=7
WEBSITE_LOG_CONTAINER_ENABLED=1
```

### Configuração do Banco de Dados (PostgreSQL)

Se estiver usando PostgreSQL:

```
DATABASE_ENGINE=postgresql
DATABASE_HOST=<seu-servidor>.postgres.database.azure.com
DATABASE_NAME=<nome-do-banco>
DATABASE_USER=<usuario>
DATABASE_PASSWORD=<senha>
DATABASE_PORT=5432
```

## Implantação via GitHub Actions

1. Configure os secrets no seu repositório GitHub:
   - `AZURE_CREDENTIALS`: JSON de credenciais do Azure Service Principal
   - `AZURE_WEBAPP_NAME`: Nome da aplicação web no Azure

2. O workflow já está configurado no arquivo `.github/workflows/azure-webapps-python.yml`

3. Faça um push para a branch main para iniciar o deployment automático

## Implantação Manual via Azure CLI

```bash
# Login no Azure
az login

# Criar grupo de recursos (se não existir)
az group create --name autoita-resources --location eastus

# Criar plano de serviço de aplicativo
az appservice plan create --name autoita-plan --resource-group autoita-resources --sku S1

# Criar aplicativo web
az webapp create --name autoitaapp --resource-group autoita-resources --plan autoita-plan --runtime "PYTHON:3.12"

# Configurar variáveis de ambiente
az webapp config appsettings set --resource-group autoita-resources --name autoitaapp --settings \
  DJANGO_SETTINGS_MODULE=PI_2.settings_production \
  DJANGO_SECRET_KEY=<sua-chave-secreta> \
  WEBSITE_HTTPLOGGING_RETENTION_DAYS=7

# Deployment via Git local
az webapp deployment source config-local-git --name autoitaapp --resource-group autoita-resources

# Adicionar remote do Azure
git remote add azure <URL-exibida-acima>

# Fazer push para o Azure
git push azure main
```

## Monitoramento e Logging

1. Acesse logs pelo portal do Azure App Service ou Azure CLI:
   ```bash
   az webapp log tail --name autoitaapp --resource-group autoita-resources
   ```

2. Configure Application Insights para monitoramento avançado:
   ```bash
   az monitor app-insights component create --app autoitaapp-insights --resource-group autoita-resources --location eastus --application-type web
   ```

## Solução de Problemas Comuns

1. **Erro 500 após o deployment**: Verifique os logs de aplicativo para detalhes específicos do erro.

2. **Problemas com arquivos estáticos**: Verifique se a variável `STATIC_ROOT` está configurada corretamente e se `collectstatic` está sendo executado.

3. **Erros de conexão com PostgreSQL**: Verifique as regras de firewall do servidor PostgreSQL para permitir conexões do Azure App Service.

## Otimização de Desempenho

1. Ative Always On nas configurações do App Service para evitar tempos de inicialização frios.

2. Configure slots de implantação para deployments sem interrupções (zero-downtime).

3. Configure CDN para arquivos estáticos para melhorar o desempenho.