variable "subscription_id" {
  type        = string
  description = "ID da assinatura Azure (az account show --query id -o tsv)"
}

variable "location" {
  type        = string
  description = "Região Azure. Se a sua assinatura bloquear esta, tente outra permitida."
  default     = "brazilsouth"
}

variable "image" {
  type        = string
  description = "Imagem no GHCR (pacote público), ex.: ghcr.io/usuario/repo:latest (tudo minúsculo)"
}

variable "api_key" {
  type        = string
  sensitive   = true
  description = "Chave que o robô envia no header X-API-Key"
}
