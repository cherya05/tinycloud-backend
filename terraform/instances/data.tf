data "terraform_remote_state" "aws_vpc" {
    backend = "s3"
    config = {
        bucket = "tinycloud.terraform"
        key    = "terraform/network/.terraform/terraform.tfstate"
        region = "eu-north-1"
    }
}

data "terraform_remote_state" "aws_subnet" {
    backend = "s3"
    config = {
        bucket = "tinycloud.terraform"
        key    = "terraform/network/.terraform/terraform.tfstate"
        region = "eu-north-1"
    }
}

data "aws_vpc" "main" {
    id = data.terraform_remote_state.aws_vpc.outputs.vpc_id
}

data "aws_subnet" "public_subnet_a" {
    id = data.terraform_remote_state.aws_subnet.outputs.public_subnet_ids[0]
}

data "aws_subnet" "private_subnet_a" {
    id = data.terraform_remote_state.aws_subnet.outputs.private_subnets_ids_az_a[0]
}

data "aws_subnet" "private_subnet_b" {
    id = data.terraform_remote_state.aws_subnet.outputs.private_subnets_ids_az_b[0]
}

#

data "aws_secretsmanager_secret" "secret_key_name" {
  name = "key_name"
}

data "aws_secretsmanager_secret_version" "key_name" {
  secret_id = data.aws_secretsmanager_secret.secret_key_name.id
}

data "aws_secretsmanager_secret" "secret_ami_version" {
  name = "ami_version"
}

data "aws_secretsmanager_secret_version" "ami_instance" {
  secret_id = data.aws_secretsmanager_secret.secret_ami_version.id
}