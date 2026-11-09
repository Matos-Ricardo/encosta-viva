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

O projeto também possui regras de alerta para ausência de leituras e aumento de respostas HTTP 5xx.

## Privacidade e LGPD

O projeto deve observar os princípios da Lei Geral de Proteção de Dados (LGPD).

- Coletar somente informações necessárias para o monitoramento.
- Evitar o armazenamento de dados pessoais desnecessários.
- Proteger credenciais e informações de acesso.
- Restringir o acesso aos recursos de infraestrutura.
- Definir políticas de retenção e tratamento dos registros.

A aplicação não deve ser utilizada como substituta dos procedimentos oficiais da Defesa Civil.

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

A infraestrutura utiliza serviços Azure, incluindo Azure Container Apps e Log Analytics.

Os custos dependem do consumo de CPU, memória, armazenamento, registros e tráfego.

A estimativa financeira detalhada deve considerar a configuração efetivamente provisionada, a região `brazilsouth` e os preços vigentes no momento da entrega.

## Links do projeto

- **Aplicação:** https://encosta-api.salmonglacier-42a3ced4.brazilsouth.azurecontainerapps.io
- **Repositório GitHub:** https://github.com/Matos-Ricardo/encosta-viva

---

Projeto acadêmico desenvolvido para a FIAP — Global Solution 2026.2.
