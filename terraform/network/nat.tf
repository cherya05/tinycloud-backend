# Elastic IP and NAT

resource "aws_eip" "main" {

    tags = {
        Name = "${var.name}-elatic-ip-a"
    }
}

resource "aws_nat_gateway" "nat_a" {
    allocation_id = aws_eip.main.id
    subnet_id = aws_subnet.public_subnet_a.id

    tags = {
        Name = "${var.name}-nat-gw-a"
    }
}

output "eip_address_main" {
    value = aws_eip.main.public_ip
}