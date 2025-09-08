resource "aws_iam_policy" "eks_cluster_policy" {
    name = "eks-cluster-policy-${var.name}"
    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = [
                    "eks:WorkerNodePolicy",
                    "eks:CNIAddonPolicy",
                    "eks:CNIDeletePolicy",
                    "eks:CNIUpdatePolicy",
                    "eks:CNIAddonPolicy",
                    "eks:CNIDeletePolicy",
                    "eks:CNIUpdatePolicy",
                    "ec2:ContainerRegistryReadOnly",
                ]
                Effect = "Allow"
                Resource = "*"
            }
        ]
    })
}

resource "aws_iam_role" "eks_cluster_role" {
    name = "eks-cluster-role-${var.name}"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = "sts:AssumeRole"
                Principal = {
                    Service = "eks.amazonaws.com"
                }
                Effect = "Allow"
        }
        ]
    })
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
    role = aws_iam_role.eks_cluster_role.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

resource "aws_iam_role_policy_attachment" "eks_service_policy" {
    role = aws_iam_role.eks_cluster_role.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
}

resource "aws_iam_role" "eks_node_group_role" {
    name = "eks-node-group-role-${var.name}"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = "sts:AssumeRole"
                Principal = {
                    Service = "ec2.amazonaws.com"
                }
                Effect = "Allow"
            }
        ]
    })
}