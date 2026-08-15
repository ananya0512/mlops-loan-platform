resource "aws_security_group" "mlflow_rds" {
  name        = "mlops-loan-mlflow-rds"
  description = "Allow PostgreSQL access from EKS"
  vpc_id      = "vpc-096bd050f02841a54"

  ingress {
    description     = "PostgreSQL from EKS"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = ["sg-0f2a8689cc4fbb6a1"]
  }

  egress {
    description = "Allow outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "mlops-loan-mlflow-rds"
    Project     = "mlops-loan-platform"
    Environment = "dev"
  }
}

resource "aws_db_subnet_group" "mlflow" {
  name = "mlops-loan-mlflow"

  subnet_ids = [
    "subnet-08b6ed53101f25bdc",
    "subnet-0b8e6d8668b174b71",
    "subnet-08bef73df552bf5ac"
  ]

  tags = {
    Name        = "mlops-loan-mlflow"
    Project     = "mlops-loan-platform"
    Environment = "dev"
  }
}

resource "aws_db_instance" "mlflow" {
  identifier = "mlops-loan-mlflow"

  engine         = "postgres"
  engine_version = "17"

  instance_class        = "db.t4g.micro"
  allocated_storage     = 20
  max_allocated_storage = 50
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name  = "mlflow"
  username = "mlflow"
  password = var.mlflow_db_password

  db_subnet_group_name   = aws_db_subnet_group.mlflow.name
  vpc_security_group_ids = [aws_security_group.mlflow_rds.id]

  publicly_accessible = false

  backup_retention_period = 0
  skip_final_snapshot     = true

  tags = {
    Name        = "mlops-loan-mlflow"
    Project     = "mlops-loan-platform"
    Environment = "dev"
    Purpose     = "mlflow-backend"
  }
}