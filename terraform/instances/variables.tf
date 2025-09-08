# variable "instance_type" {
#     description = "Instance type"
#     type = string
# }

variable "aws_region" {
    description = "AWS region"
    type = string
}

variable "name" {
    description = "Name"
    type = string
}

variable "ec2_security_group_description" {
    description = "Description for the EC2 security group"
    type = string
}

variable "cidr_block" {
    description = "CIDR block"
    type = list(string)
}

# variable "public_key_path" {
#     description = "Public key path"
#     type = string
# }