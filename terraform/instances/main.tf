terraform {
    backend "s3" {
        bucket = "tinycloud.terraform"
        key = "terraform/instances/.terraform/terraform.tfstate"
        region = "eu-north-1"
    }
}

provider "aws" {
    region = "eu-north-1"
}