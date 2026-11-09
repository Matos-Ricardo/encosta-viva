# Passo a passo para publicar (PowerShell)

Pré-requisitos instalados: Git, Docker Desktop, Terraform e Azure CLI. Contas: GitHub e Azure.

## 1. Subir o código para um repositório público no GitHub

Crie um repositório público vazio no GitHub e, na pasta do projeto:

```powershell
git init -b main
git add .
git commit -m "Encosta Viva - versão inicial"
git remote add origin https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
git push -u origin main
```

O pipeline roda sozinho. Nesta primeira vez ele para antes do deploy (ainda não configuramos a Azure) e publica a imagem no GHCR.

## 2. Tornar a imagem pública no GHCR

GitHub, seu perfil, aba **Packages**, abra o pacote, **Package settings**, **Change visibility**, **Public**.
Anote o nome da imagem, tudo em minúsculas: `ghcr.io/seu-usuario/seu-repositorio:latest`.

## 3. Testar local (print para o PDF)

```powershell
Copy-Item .env.example .env     # edite o .env: API_KEY e GRAFANA_PASSWORD
docker compose up --build
Invoke-RestMethod http://localhost:8000/saude
Invoke-RestMethod -Method Post -Uri http://localhost:8000/leituras -Headers @{"X-API-Key"="SUA-CHAVE"} -ContentType "application/json" -Body '{"setor_id":"vila-sahy","umidade_pct":82,"nivel":"ALERTA"}'
```

## 4. Criar a infraestrutura na Azure com Terraform

```powershell
az login
az account show --query id -o tsv                      # copie o ID da assinatura
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights

cd infra
Copy-Item terraform.tfvars.example terraform.tfvars    # edite: subscription_id, image, api_key
terraform init
terraform plan
terraform apply
```

Ao final, o Terraform mostra `url = "https://encosta-api...azurecontainerapps.io"`. Teste `<url>/saude` no navegador.
Se der erro de região ou política, troque `location` no `terraform.tfvars` por outra região permitida na sua assinatura.

## 5. Ligar o deploy automático

Crie a conta de serviço que o GitHub usa para atualizar o Container App (troque `ID-DA-ASSINATURA`):

```powershell
az ad sp create-for-rbac --name gh-encosta-deploy --role contributor --scopes /subscriptions/ID-DA-ASSINATURA/resourceGroups/rg-encosta-viva --sdk-auth
```

No GitHub: **Settings, Secrets and variables, Actions**:

- Secret `AZURE_CREDENTIALS`: cole o JSON inteiro que o comando mostrou.
- Variable `DEPLOY_ENABLED`: `true`.

Faça qualquer commit em `main` (ou rode o workflow de novo). O último passo do pipeline troca a imagem do Container App.

> Se a sua conta da faculdade bloquear a criação do service principal, avise para trocarmos o deploy por outra forma.

## 6. Prometheus e Grafana apontando para a nuvem

Edite `monitoring/prometheus.yml`: no job `api-nuvem`, troque o alvo pelo host da URL do Terraform (sem `https://`). Depois:

```powershell
docker compose up -d
```

- Grafana: http://localhost:3000 (dashboard "Encosta Viva - 4 sinais de ouro" já vem pronto)
- Prometheus: http://localhost:9090/alerts

Mande leituras para a URL pública (o robô ou o `Invoke-RestMethod` com a URL da nuvem) para o dashboard ter dados.

**Alerta disparado:** pare de enviar leituras por cerca de 6 minutos. O alerta `SemLeiturasDoSensor` vai para **FIRING** em
http://localhost:9090/alerts (tire o print). Volte a enviar leituras e ele resolve.

## 7. Demonstração do pipeline barrado e corrigido

**Gitleaks (segredo vazado):**

```powershell
git checkout -b teste-segredo
$t = "123456789:A" + (-join ((48..57)+(65..90)+(97..122) | Get-Random -Count 34 | ForEach-Object {[char]$_}))
"TELEGRAM_BOT_TOKEN = `"$t`"" | Out-File app/config_teste.py -Encoding utf8
git add . ; git commit -m "teste: token falso" ; git push -u origin teste-segredo
```

Tire print da execução **vermelha** (job Gitleaks falhou). Depois remova e envie de novo:

```powershell
git rm app/config_teste.py
git commit -m "remove token falso" ; git push
```

Tire print da execução **verde**. Se o Gitleaks continuar acusando o commit antigo, reescreva a branch de teste:
`git reset --hard HEAD~2` seguido de `git push --force`, e rode de novo.
(O token é gerado na hora, por isso nenhum segredo de mentira fica gravado nos arquivos do repositório.)

**Trivy (configuração insegura):**

```powershell
git checkout main
git checkout -b teste-trivy
```

No `Dockerfile`, coloque `#` na frente da linha `USER appuser` e envie. O Trivy acusa "Image user should not be root"
(execução **vermelha**). Descomente a linha, envie de novo e tire o print da execução **verde**.

## 8. Checklist de evidências para o PDF

- [ ] `docker compose up` rodando (print)
- [ ] `terraform apply` concluído e URL pública funcionando (prints)
- [ ] Pipeline verde completo, mais as execuções vermelha e corrigida do Gitleaks e do Trivy
- [ ] Dashboard do Grafana com os 4 sinais e o alerta em FIRING (prints)
- [ ] Diagrama, matriz de responsabilidade e onde ficam os dados pessoais (`docs/ARQUITETURA.md`)
- [ ] Estimativa de custo (print da calculadora da Azure)
- [ ] Nomes completos e RMs de todos, links clicáveis do repositório e da URL do MVP
- [ ] Um único PDF enviado por uma pessoa da equipe no portal da disciplina até 19/11, 23h55
