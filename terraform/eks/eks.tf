resource "aws_eks_cluster" "main" {
    name = "eks-cluster-${var.name}"

    role_arn = aws_iam_role.eks_cluster_role.arn

    vpc_config {
        subnet_ids = data.aws_subnets.private_subnets.ids
    }

    depends_on = [aws_iam_role_policy_attachment.eks_cluster_policy]
}