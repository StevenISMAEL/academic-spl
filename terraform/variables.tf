variable "project_id" {
  description = "ID del proyecto en Google Cloud"
  type        = string
  default     = "academic-spl-devops"
}

variable "region" {
  description = "Región de GCP donde se desplegarán los recursos"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "Zona de GCP para el clúster GKE"
  type        = string
  default     = "us-central1-a"
}

variable "gke_name" {
  description = "Nombre del clúster de GKE"
  type        = string
  default     = "gke-academic-spl"
}

variable "db_name" {
  description = "Nombre de la instancia de Cloud SQL"
  type        = string
  default     = "academic-spl-postgres"
}

variable "db_user" {
  description = "Usuario administrador de la base de datos"
  type        = string
  default     = "academicsqladmin"
}

variable "db_password" {
  description = "Contraseña de la base de datos (inyectada por CI/CD como secreto)"
  type        = string
  sensitive   = true
}
