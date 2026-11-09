output "url" {
  description = "URL pública do MVP"
  value       = "https://${azurerm_container_app.api.ingress[0].fqdn}"
}
