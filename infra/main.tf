
terraform {
  required_version = ">= 1.5"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }

  # State LOCAL de propósito.
  # O arquivo terraform.tfstate deve permanecer no .gitignore.
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "rg-encosta-viva"
  location = var.location
}

# Log Analytics
resource "azurerm_log_analytics_workspace" "log" {
  name                = "log-encosta-viva"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

# Container Apps Environment
resource "azurerm_container_app_environment" "env" {
  name                       = "env-encosta-viva"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.log.id

  workload_profile {
    name                  = "Consumption"
    workload_profile_type = "Consumption"
    minimum_count         = 0
    maximum_count         = 0
  }
}

# Container App - API
resource "azurerm_container_app" "api" {
  name                         = "encosta-api"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = azurerm_resource_group.rg.name
  revision_mode                = "Single"

  # Segredo da API
  secret {
    name  = "api-key"
    value = var.api_key
  }

  template {
    min_replicas = 1
    max_replicas = 1

    container {
      name   = "api"
      image  = var.image
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name        = "API_KEY"
        secret_name = "api-key"
      }
    }
  }

  # Ingress externo
  ingress {
    external_enabled = true
    target_port      = 8000
    transport        = "auto"

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  # O GitHub Actions controla as atualizações das imagens.
  # O Terraform não deve sobrescrever a imagem publicada pelo pipeline.
  lifecycle {
    ignore_changes = [template[0].container[0].image]
  }
}
