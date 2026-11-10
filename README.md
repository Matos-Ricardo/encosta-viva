# Encosta Viva

**Sistema de alerta antecipado de deslizamentos para comunidades que vivem em áreas de risco.**

Projeto desenvolvido para a disciplina **Secure DevOps Tools & Cloud Computing**, FIAP Global Solution 2026.2 — CitizenTech — 4ES.

## Integrantes

| Nome completo | RM |
|---|---|
| Ricardo Matos | 95906 |
| Julio Zampieri | 98772 |
| João Dias | 99092 |

## Ficha Técnica do MVP

| Campo | Descrição |
|---|---|
| Nome do produto | Encosta Viva |
| Público-alvo | Moradores de áreas de risco de deslizamento e agentes da Defesa Civil municipal. |
| Problema | Alertas genéricos por município podem não oferecer informações suficientemente específicas sobre o risco enfrentado por cada comunidade. |
| Proposta de valor | Centralizar informações de monitoramento e disponibilizar alertas por setor de risco, com orientações claras para a população. |
| API | Python, FastAPI e Uvicorn. |
| Infraestrutura | Azure Container Apps e Azure Log Analytics. |
| Containerização | Docker e Docker Compose. |
| Infraestrutura como código | Terraform. |
| CI/CD e segurança | GitHub Actions, Gitleaks, Semgrep e Trivy. |
| Observabilidade | Prometheus e Grafana. |
| URL do MVP | https://encosta-api.salmonglacier-42a3ced4.brazilsouth.azurecontainerapps.io |
| Repositório | https://github.com/Matos-Ricardo/encosta-viva |
| Indicadores de impacto | Antecedência dos alertas, quantidade de leituras recebidas, disponibilidade da API e ocorrência de falsos alarmes. |
| ODS relacionados | ODS 3, 9, 10, 11 e 13. |

## Arquitetura da solução

O Encosta Viva utiliza uma arquitetura baseada em serviços containerizados e infraestrutura em nuvem.

Principais componentes:

- **API FastAPI:** recebe e disponibiliza informações relacionadas ao monitoramento.
- **Docker:** empacota a aplicação em um container.
- **Azure Container Apps:** hospeda a aplicação na nuvem.
- **Terraform:** provisiona os recursos de infraestrutura.
- **GitHub Actions:** automatiza testes, verificações de segurança, publicação da imagem e deploy.
- **Prometheus:** coleta métricas da aplicação.
- **Grafana:** disponibiliza painéis para visualização das métricas.
- **Azure Log Analytics:** centraliza registros da infraestrutura.

## Estrutura do repositório

```text
app/
  API FastAPI e testes

Dockerfile
  Construção da imagem da aplicação

docker-compose.yml
  Inicialização dos serviços locais

monitoring/
  Configuração do Prometheus
  Regras de alertas
  Dashboard Grafana

infra/
  Arquivos Terraform

.github/workflows/
  Pipeline CI/CD

docs/
  Documentação do projeto
```

## Como executar localmente

Pré-requisitos:

- Docker
- Docker Compose
- Git

No terminal, execute:

```bash
docker compose up --build -d
```

Configure previamente as variáveis de ambiente necessárias no arquivo `.env`, utilizando o `.env.example` como referência.

### Serviços disponíveis

| Serviço | Endereço |
|---|---|
| API | http://localhost:8000 |
| Documentação da API | http://localhost:8000/docs |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

## Contrato da API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/saude` | Verifica a disponibilidade da API. |
| POST | `/leituras` | Recebe informações de leitura do monitoramento. |
| GET | `/setores/{id}/risco` | Consulta o nível de risco de um setor. |
| GET | `/metrics` | Disponibiliza métricas para o Prometheus. |

A rota `/leituras` utiliza autenticação por chave de API no cabeçalho `X-API-Key`.

Níveis previstos:

- `NORMAL`
- `ATENCAO`
- `ALERTA`
- `ERRO`

## Segurança e DevSecOps

O projeto utiliza práticas de segurança durante o desenvolvimento e a publicação:

- Imagem Docker baseada em imagem slim e construção multi-stage.
- Execução da aplicação com usuário não-root.
- Segredos fornecidos por variáveis de ambiente e mecanismos de secrets.
- Gitleaks para identificação de segredos expostos.
- Semgrep para análise estática do código.
- Trivy para verificação de vulnerabilidades.
- GitHub Actions para automatização do processo de integração e entrega.
- Terraform para gerenciamento da infraestrutura.

Arquivos sensíveis, como `.env`, `.tfvars` e arquivos de estado do Terraform, são excluídos do versionamento por meio do `.gitignore`.

## Monitoramento e observabilidade

O monitoramento utiliza Prometheus e Grafana.

As métricas acompanhadas incluem os quatro sinais de ouro:

1. **Latência:** tempo de resposta das requisições.
2. **Tráfego:** quantidade de requisições recebidas.
3. **Erros:** proporção de respostas com falha.
4. **Saturação:** utilização de CPU e memória.

O Prometheus coleta métricas da API local e da aplicação publicada no Azure.

O Azure Monitor possui uma regra de alerta para identificar respostas HTTP 500 nos logs da aplicação, com avaliação a cada cinco minutos e envio configurado por meio de um Action Group.

**Limitação do teste:** a regra foi criada e habilitada, mas não houve comprovação de disparo real durante a validação. O teste nativo de notificações do Action Group foi bloqueado pela assinatura Azure for Students (mensagem `Free subscription not supported`). Portanto, o envio de notificações permanece configurado, mas não foi validado por um disparo efetivo.

## Privacidade e LGPD

A versão atual do Encosta Viva não possui cadastro de moradores nem solicita diretamente dados pessoais, como nome, CPF, telefone ou endereço.

A API recebe e processa os seguintes dados:
- `setor_id`: identificação do setor monitorado;
- `umidade_pct`: percentual de umidade do solo;
- `nivel`: classificação da situação do setor;
- `recebido_em`: horário de recebimento da leitura.

As últimas leituras são mantidas em memória durante a execução da aplicação, sem persistência em banco de dados nesta versão do MVP.

O identificador do setor não deve ser associado publicamente a uma pessoa identificável. Caso essa associação seja necessária em versões futuras, deverão ser adotadas medidas adicionais de proteção, controle de acesso e minimização de dados.

As credenciais de acesso são fornecidas por variáveis de ambiente, e o envio das leituras é protegido por chave de API.

Os registros de infraestrutura e monitoramento devem ter acesso restrito e políticas de retenção adequadas.

O projeto deve observar os princípios da Lei Geral de Proteção de Dados (LGPD), especialmente finalidade, necessidade, segurança e prevenção.

**Limitação:** o Encosta Viva é um MVP acadêmico e não substitui os procedimentos oficiais da Defesa Civil.

## Responsabilidade compartilhada

| Responsabilidade | Projeto | Provedor Azure |
|---|---|---|
| Código da aplicação | Responsável | — |
| Configuração do container | Responsável | Infraestrutura de execução |
| Gerenciamento de credenciais | Responsável | Recursos de armazenamento de secrets |
| Segurança do código | Responsável | — |
| Segurança física dos datacenters | — | Responsável |
| Disponibilidade da infraestrutura de nuvem | — | Responsável conforme serviço contratado |
| Monitoramento da aplicação | Responsável | Ferramentas de infraestrutura disponíveis |

## Estimativa de custos

A infraestrutura utiliza serviços Azure na região `brazilsouth`, incluindo Azure Container Apps e Log Analytics.

O workspace do Log Analytics utiliza SKU `PerGB2018`, retenção de 30 dias e não possui limite diário de ingestão configurado.

Na consulta dos últimos 30 dias, foram identificados **0,0001 GB de dados faturáveis ingeridos** (aproximadamente 0,1 MB).

Na consulta ao Cost Analysis do Azure em **10/11/2026**, o custo real acumulado de novembro era de **R$ 0,84**, distribuído entre Azure Container Apps (R$ 0,68), Azure Monitor (R$ 0,16) e Log Analytics (R$ 0,00).

A extrapolação linear desse consumo para 30 dias resulta em aproximadamente **R$ 2,52**. Trata-se de uma estimativa própria, não de uma previsão oficial do Azure. O custo efetivo pode variar conforme o consumo dos recursos e os preços regionais.

Para simulações, consulte a [calculadora oficial da Azure](https://azure.microsoft.com/pricing/calculator/).

## Links do projeto

- **Aplicação:** https://encosta-api.salmonglacier-42a3ced4.brazilsouth.azurecontainerapps.io
- **Repositório GitHub:** https://github.com/Matos-Ricardo/encosta-viva

---

Projeto acadêmico desenvolvido para a FIAP — Global Solution 2026.2.
