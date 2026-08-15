data "aws_iam_policy_document" "mlflow_s3_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.eks.arn]
    }

    actions = [
      "sts:AssumeRoleWithWebIdentity"
    ]

    condition {
      test     = "StringEquals"
      variable = "oidc.eks.ap-south-1.amazonaws.com/id/F168812A8F170F3BCDAFB61702579F06:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "oidc.eks.ap-south-1.amazonaws.com/id/F168812A8F170F3BCDAFB61702579F06:sub"
      values = [
        "system:serviceaccount:mlops:mlflow"
      ]
    }
  }
}


resource "aws_iam_openid_connect_provider" "eks" {
  url = "https://oidc.eks.ap-south-1.amazonaws.com/id/F168812A8F170F3BCDAFB61702579F06"

  client_id_list = [
    "sts.amazonaws.com"
  ]
}


resource "aws_iam_role" "mlflow" {
  name = "mlops-loan-mlflow-s3-role"

  assume_role_policy = data.aws_iam_policy_document.mlflow_s3_assume_role.json

  tags = {
    Project     = "mlops-loan-platform"
    Environment = "dev"
    Purpose     = "mlflow-s3-access"
  }
}


data "aws_iam_policy_document" "mlflow_s3" {
  statement {
    effect = "Allow"

    actions = [
      "s3:ListBucket"
    ]

    resources = [
      aws_s3_bucket.mlflow_artifacts.arn
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject"
    ]

    resources = [
      "${aws_s3_bucket.mlflow_artifacts.arn}/*"
    ]
  }
}


resource "aws_iam_role_policy" "mlflow_s3" {
  name = "mlflow-s3-access"
  role = aws_iam_role.mlflow.id

  policy = data.aws_iam_policy_document.mlflow_s3.json
}


output "mlflow_iam_role_arn" {
  description = "IAM role used by the MLflow Kubernetes ServiceAccount"
  value       = aws_iam_role.mlflow.arn
}