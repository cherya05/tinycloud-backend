resource "aws_eks_cluster" "main" {
    name = "eks-cluster-${var.name}"

    role_arn = aws_iam_role.eks_cluster_role.arn

    vpc_config {
        subnet_ids = [
            data.aws_subnet.private_subnet_a.id,
            data.aws_subnet.private_subnet_b.id,
        ]
    }

    depends_on = [aws_iam_role_policy_attachment.eks_cluster_policy]
}