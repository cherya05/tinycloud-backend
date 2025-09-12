data "terraform_remote_state" "aws_vpc" {
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

data "aws_subnets" "private_subnets" {
    filter {
        name = "vpc-id"
        values = [data.terraform_remote_state.aws_vpc.outputs.vpc_id]
    }
}

data "aws_subnet" "private_subnets" {
    for_each = toset(data.aws_subnets.private_subnets.ids)
    id = each.value
}

output "subnet_cidr_blocks" {
  value = [for subnet in data.aws_subnet.private_subnets : subnet.cidr_block] 
}


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