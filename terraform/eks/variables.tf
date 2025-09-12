variable "aws_region" {
    description = "AWS region"
    type = string
}

variable "name" {
    description = "Name"
    type = string
}

variable "cidr_block" {
    description = "CIDR block"
    type = list(string)
}