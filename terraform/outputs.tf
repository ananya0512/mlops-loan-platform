output "mlflow_artifacts_bucket_name" {
  description = "S3 bucket used for MLflow artifacts"
  value       = aws_s3_bucket.mlflow_artifacts.bucket
}

output "mlflow_artifacts_bucket_arn" {
  description = "ARN of the MLflow artifacts S3 bucket"
  value       = aws_s3_bucket.mlflow_artifacts.arn
}

output "mlflow_db_endpoint" {
  description = "RDS PostgreSQL endpoint for MLflow"
  value       = aws_db_instance.mlflow.address
}

output "mlflow_db_port" {
  description = "RDS PostgreSQL port"
  value       = aws_db_instance.mlflow.port
}