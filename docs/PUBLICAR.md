# Guia de publicação — Encosta Viva

Este documento apresenta a configuração, execução, publicação e monitoramento do projeto Encosta Viva, desenvolvido para a FIAP Global Solution 2026.2.

## 1. Pré-requisitos

Ferramentas necessárias:

- Git
- Docker Desktop ou Docker Engine
- Terraform
- Azure CLI
- Conta no GitHub
- Conta na Microsoft Azure

Repositório: https://github.com/Matos-Ricardo/encosta-viva

## 2. Publicação da imagem no GitHub Container Registry (GHCR)

O projeto utiliza o GitHub Container Registry para armazenar a imagem Docker.

O workflow do GitHub Actions constrói e publica automaticamente a imagem quando ocorre um push na branch `main`.

O nome da imagem segue o padrão:

```text
ghcr.io/matos-ricardo/encosta-viva:latest
```

A imagem deve estar com visibilidade pública para permitir que o Azure Container Apps faça o download sem autenticação privada.

Para conferir a visibilidade:

1. Acesse o perfil do GitHub.
2. Entre na aba Packages.
3. Abra o pacote `encosta-viva`.
4. Acesse Package settings.
5. Confira se a visibilidade está como Public.

## 3. Executar o projeto localmente

Na raiz do repositório, copie o arquivo de exemplo das variáveis de ambiente:

```powershell
Copy-Item .env.example .env
```

Edite o `.env` e configure os valores necessários, como `API_KEY` e `GRAFANA_PASSWORD`.

Não compartilhe nem versione o arquivo `.env`.

Inicie os serviços:

```bash
docker compose up --build -d
```

Confira os containers:

```bash
docker compose ps
```

Teste a saúde da API:

```powershell
Invoke-RestMethod http://localhost:8000/saude
```

Envie uma leitura de teste:

```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/leituras" -Headers @{"X-API-Key"="SUA-CHAVE"} -ContentType "application/json" -Body '{"setor_id":"vila-sahy","umidade_pct":82,"nivel":"ALERTA"}'
```

Substitua `SUA-CHAVE` pela chave configurada no ambiente.

## 4. Infraestrutura na Azure com Terraform

A infraestrutura do Encosta Viva é provisionada na Microsoft Azure utilizando Terraform.

### Recursos provisionados

- Azure Resource Group: `rg-encosta-viva`
- Azure Container Apps Environment
- Azure Container App: `encosta-api`
- Log Analytics Workspace

Região utilizada: `brazilsouth`.

### Configuração do projeto atual

O estado do Terraform e as variáveis sensíveis ficam fora do repositório, em diretório protegido:

- Estado: `/workspaces/encosta-viva-state/terraform.tfstate`
- Variáveis: `/workspaces/encosta-viva-state/terraform.tfvars`
- Backend local configurado em `infra/main.tf`.

O arquivo `infra/terraform.tfvars.example` contém apenas valores ilustrativos e serve como referência para uma nova instalação.

**Importante:** não execute `terraform init -migrate-state` nem `terraform apply` na infraestrutura já existente sem revisar previamente o estado e o plano. O estado atual deve ser preservado.

Para consultar os recursos registrados no estado:

```bash
cd infra
terraform state list
```

Para consultar a configuração da infraestrutura:

```bash
```

Em uma nova instalação, será necessário configurar uma assinatura Azure, preencher as variáveis sensíveis fora do repositório e inicializar o Terraform com um backend adequado ao novo ambiente.

O caminho local configurado atualmente depende do Codespace onde o projeto foi desenvolvido e não deve ser considerado um caminho universal.

### Teste da API publicada

A API está disponível em:

https://encosta-api.salmonglacier-42a3ced4.brazilsouth.azurecontainerapps.io

Teste o endpoint:

```text
https://encosta-api.salmonglacier-42a3ced4.brazilsouth.azurecontainerapps.io/saude
```

A resposta esperada é:

```json
{
  "status": "ok"
}
```

## 5. Deploy automático pela GitHub Actions

O deploy automático do Encosta Viva está configurado no workflow:

```text
.github/workflows/
```

O processo é executado em eventos de push na branch `main` e possui as seguintes etapas:

1. Testes automatizados com Pytest.
2. Verificação de segredos com Gitleaks.
3. Análise estática de código com Semgrep.
4. Construção da imagem Docker.
5. Análise de vulnerabilidades da imagem com Trivy.
6. Análise de configurações do Dockerfile e Terraform com Trivy.
7. Publicação da imagem no GitHub Container Registry (GHCR).
8. Atualização da imagem do Azure Container App.

O deploy na Azure depende de duas configurações no GitHub:

- Secret `AZURE_CREDENTIALS`: credenciais da aplicação de serviço autorizada na Azure.
- Variable `DEPLOY_ENABLED`: deve estar definida como `true`.

Essas configurações ficam em:

**GitHub → Settings → Secrets and variables → Actions.**

O deploy é realizado somente em eventos de push na branch `main`, quando as verificações anteriores são aprovadas e as configurações necessárias estão habilitadas.

O Container App atualizado utiliza o nome `encosta-api`, no Resource Group `rg-encosta-viva`.

### Evidências de segurança

O projeto possui execuções do pipeline que demonstram tanto o bloqueio de vulnerabilidades quanto a execução corrigida.

As evidências podem ser consultadas na aba Actions do repositório.

## 6. Prometheus e Grafana apontando para a nuvem

O projeto utiliza Prometheus para coleta de métricas e Grafana para visualização e monitoramento.

O arquivo de configuração do Prometheus está em:

```text
monitoring/prometheus.yml
```

O monitoramento contempla dois alvos:

- API local: `api:8000`
- API publicada: Azure Container Apps.

Para iniciar os serviços de monitoramento:

```bash
docker compose up -d
```

Endereços locais:

- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090
- Prometheus Alerts: http://localhost:9090/alerts

O Grafana utiliza o datasource Prometheus e possui um dashboard destinado ao acompanhamento dos quatro sinais de monitoramento.

### Teste de envio de leituras

Para gerar métricas e alimentar o monitoramento, envie leituras para a API publicada utilizando o endpoint `/leituras` e a chave de autenticação configurada.

### Teste do alerta

O projeto possui o alerta `SemLeiturasDoSensor`, destinado a identificar a ausência de novas leituras.

Para testar:

1. Interrompa temporariamente o envio de leituras.
2. Aguarde aproximadamente seis minutos, conforme a configuração da regra.
3. Acesse `http://localhost:9090/alerts`.
4. Verifique se o alerta aparece como FIRING.
5. Retome o envio de leituras e acompanhe a resolução do alerta.

O teste deve ser documentado com uma captura de tela quando executado.

## 7. Demonstração do pipeline de segurança

O projeto utiliza Gitleaks, Semgrep e Trivy para verificar problemas de segurança durante a integração e publicação.

As execuções do GitHub Actions permitem demonstrar o bloqueio de problemas identificados e a aprovação após as correções.

### Gitleaks

O Gitleaks verifica a presença de possíveis segredos no código e no histórico do repositório.

A evidência de execução pode ser obtida na aba Actions, mostrando o resultado do job `gitleaks`.

Não utilize credenciais reais para simular vazamentos. Caso seja necessário realizar um teste controlado, utilize apenas dados sintéticos e uma branch temporária.

### Semgrep

O Semgrep realiza análise estática do código, utilizando as regras:

- `p/python`
- `p/dockerfile`

O job é considerado aprovado quando não são encontrados problemas que bloqueiem a execução.

### Trivy

O Trivy realiza duas verificações:

- Vulnerabilidades HIGH e CRITICAL na imagem Docker, desconsiderando vulnerabilidades sem correção disponível.
- Problemas de configuração no Dockerfile e nos arquivos Terraform.

As execuções do pipeline permitem demonstrar o bloqueio por vulnerabilidades e a aprovação após os ajustes necessários.

## 8. Checklist de evidências para o PDF

Antes da entrega, reunir as seguintes evidências:

- [ ] Docker Compose executando os serviços.
- [ ] API local respondendo ao endpoint `/saude`.
- [ ] Infraestrutura provisionada na Azure.
- [ ] URL pública da API funcionando.
- [ ] Pipeline CI/CD com execução aprovada.
- [ ] Evidência de execução bloqueada por verificação de segurança.
- [ ] Evidência de execução corrigida e aprovada.
- [ ] Prometheus monitorando os alvos.
- [ ] Dashboard Grafana com os quatro sinais de monitoramento.
- [ ] Alerta `SemLeiturasDoSensor` em estado FIRING.
- [ ] Diagrama de arquitetura e matriz de responsabilidade.
- [ ] Documentação sobre a localização dos dados e LGPD.
- [ ] Estimativa de custos da infraestrutura Azure.
- [ ] Nomes completos e RMs dos integrantes.
- [ ] Links do repositório e da API pública.

## 9. Entrega final

A documentação, as evidências e os resultados do projeto devem ser reunidos em um único arquivo PDF.

A entrega deverá ser realizada por uma pessoa da equipe no portal da disciplina até:

**19/11/2026, às 23h55.**

Repositório do projeto:

https://github.com/Matos-Ricardo/encosta-viva

API publicada:

https://encosta-api.salmonglacier-42a3ced4.brazilsouth.azurecontainerapps.io