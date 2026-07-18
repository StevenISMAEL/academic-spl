terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  # Backend remoto en Google Cloud Storage
  # IMPORTANTE: Crea este bucket manualmente en GCP antes de ejecutar terraform init:
  #   gsutil mb -p <GCP_PROJECT_ID> gs://tf-state-academic-spl
  backend "gcs" {
    bucket = "tf-state-academic-spl"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}
