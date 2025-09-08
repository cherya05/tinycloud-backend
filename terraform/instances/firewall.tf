resource "aws_security_group" "server-sg" {
    name = "ec2-sg-${var.name}"
    description = var.ec2_security_group_description

    vpc_id = data.terraform_remote_state.aws_vpc.outputs.vpc_id

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = var.cidr_block
    }
    
    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = var.cidr_block
    }

    ingress {
        from_port = 443
        to_port = 443
        protocol = "tcp"
        cidr_blocks = var.cidr_block
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
    tags = {
        Name = "server-sg-${var.name}"
    }
}