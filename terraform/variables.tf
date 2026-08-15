variable "mlflow_db_password" {
  description = "Password for the MLflow PostgreSQL database"
  type        = string
  sensitive   = true
}