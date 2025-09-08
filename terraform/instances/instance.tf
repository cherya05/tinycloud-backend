# resource "aws_key_pair" "main" {
#     public_key = file(var.public_key_path)
#     key_name = data.aws_secretsmanager_secret_version.key_name.secret_string
#     tags = {
#         Name = "${var.name}-key"
#     }
# }

# resource "aws_instance" "main" {
#     ami = jsondecode(data.aws_secretsmanager_secret_version.ami_instance.secret_string).ami_version
#     instance_type = var.instance_type
#     subnet_id = data.aws_subnet.public_subnet_a.id
#     security_groups = [aws_security_group.server-sg.id]
#     key_name = jsondecode(data.aws_secretsmanager_secret_version.key_name.secret_string).keyName

    
#     tags = {
#         Name = "${var.name}-instance"
#     }
# }