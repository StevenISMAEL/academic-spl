output "gke_cluster_name" {
  value       = google_container_cluster.gke.name
  description = "Nombre del clúster GKE de academic-spl"
}

output "gke_cluster_endpoint" {
  value       = google_container_cluster.gke.endpoint
  description = "Endpoint del clúster GKE"
  sensitive   = true
}

output "postgres_connection_ip" {
  value       = google_sql_database_instance.postgres.public_ip_address
  description = "IP pública de Cloud SQL para conexión desde el pipeline CI/CD"
}

output "postgres_instance_name" {
  value       = google_sql_database_instance.postgres.name
  description = "Nombre de la instancia Cloud SQL (para el comando gcloud sql instances describe)"
}
