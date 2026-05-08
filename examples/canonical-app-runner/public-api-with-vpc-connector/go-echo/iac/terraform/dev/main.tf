terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.40" }
    awscc = { source = "hashicorp/awscc", version = "~> 1.0" }
  }
}

variable "environment" { type = string }
variable "region" { type = string }
variable "vpc_id" {
  type    = string
  default = "vpc-replace-me-dev"
}
variable "subnet_ids" {
  type    = list(string)
  default = ["subnet-replace-me-dev-a", "subnet-replace-me-dev-b"]
}

provider "aws" {
  region = var.region
}

provider "awscc" {
  region = var.region
}

locals {
  name_prefix = "accb-${var.environment}-apprunner-vpc"
  tags        = { ManagedBy = "accb", Environment = var.environment, Family = "canonical-app-runner" }
}

resource "aws_iam_role" "service" {
  name = "${local.name_prefix}-service-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Effect = "Allow", Principal = { Service = "tasks.apprunner.amazonaws.com" }, Action = "sts:AssumeRole" }]
  })
  tags = local.tags
}

resource "aws_iam_role" "access" {
  name = "${local.name_prefix}-access-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Effect = "Allow", Principal = { Service = "build.apprunner.amazonaws.com" }, Action = "sts:AssumeRole" }]
  })
  tags = local.tags
}

resource "aws_ecr_repository" "service" {
  name = "${local.name_prefix}-repo"
  image_scanning_configuration {
    scan_on_push = true
  }
  tags = local.tags
}

resource "awscc_secretsmanager_secret" "db_dev" {
  name = "/accb/${var.environment}/apprunner/vpc/db"
  tags = local.tags
}

resource "aws_security_group" "connector" {
  name        = "${local.name_prefix}-connector"
  description = "App Runner VPC connector for ${var.environment}"
  vpc_id      = var.vpc_id
  tags        = local.tags
}

resource "aws_security_group" "db" {
  name        = "${local.name_prefix}-db"
  description = "Aurora Postgres for ${var.environment}"
  vpc_id      = var.vpc_id
  tags        = local.tags
}

resource "aws_db_subnet_group" "db" {
  name       = "${local.name_prefix}-db"
  subnet_ids = var.subnet_ids
  tags       = local.tags
}

resource "aws_rds_cluster" "aurora" {
  cluster_identifier        = "${local.name_prefix}-aurora"
  engine                    = "aurora-postgresql"
  database_name             = "app"
  manage_master_user_password = true
  db_subnet_group_name      = aws_db_subnet_group.db.name
  vpc_security_group_ids    = [aws_security_group.db.id]
  tags                      = local.tags
}

resource "aws_apprunner_vpc_connector" "connector" {
  vpc_connector_name = "${local.name_prefix}-connector"
  subnets            = var.subnet_ids
  security_groups    = [aws_security_group.connector.id]
  tags               = local.tags
}

resource "aws_apprunner_service" "service" {
  service_name = "${local.name_prefix}-service"

  source_configuration {
    auto_deployments_enabled = true
    authentication_configuration {
      access_role_arn = aws_iam_role.access.arn
    }
    image_repository {
      image_identifier      = "${aws_ecr_repository.service.repository_url}:dev"
      image_repository_type = "ECR"
      image_configuration {
        port = "8080"
        runtime_environment_variables = {
          DB_HOST        = aws_rds_cluster.aurora.endpoint
          DB_SECRET_PATH = awscc_secretsmanager_secret.db_dev.name
        }
      }
    }
  }

  instance_configuration {
    instance_role_arn = aws_iam_role.service.arn
  }

  network_configuration {
    egress_configuration {
      egress_type       = "VPC"
      vpc_connector_arn = aws_apprunner_vpc_connector.connector.arn
    }
  }

  tags = local.tags
}
