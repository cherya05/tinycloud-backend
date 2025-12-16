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

resource "aws_iam_role_policy_attachment" "eks_worker_node_policy" {
    role = aws_iam_role.eks_node_group_role.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}

resource "aws_iam_role_policy_attachment" "eks_cni_policy" {
    role = aws_iam_role.eks_node_group_role.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}

resource "aws_iam_role_policy_attachment" "eks_container_registry_policy" {
    role = aws_iam_role.eks_node_group_role.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_iam_openid_connect_provider" "main" {
    client_id_list = ["sts.amazonaws.com"]
    thumbprint_list = [data.tls_certificate.eks.certificates[0].sha1_fingerprint]
    url = aws_eks_cluster.main.identity[0].oidc[0].issuer

    tags = {
        Name = "${var.name}-eks-irsa"
    }
}

resource "aws_iam_role" "external_dns_role" {
    for_each = toset(local.environments)

    name = "external-dns-${each.key}-role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = "sts:AssumeRoleWithWebIdentity"
                Effect = "Allow"
                Principal = {
                    Federated = aws_iam_openid_connect_provider.main.arn
                }
                Condition = {
                    StringEquals = {
                        "${replace(aws_eks_cluster.main.identity[0].oidc[0].issuer, "https://", "")}:sub" = "system:serviceaccount:${local.env_config[each.key].namespace}:${local.env_config[each.key].serviceaccount}"
                        "${replace(aws_eks_cluster.main.identity[0].oidc[0].issuer, "https://", "")}:aud" = "sts.amazonaws.com"
                    }
                }
            }
        ]
    })

    tags = {
        Name = "external-dns-${each.key}-role"
        Environment = each.key
    }

}

resource "aws_iam_policy" "external_dns" {
    for_each = toset(local.environments)
    
    name = "external-dns-${each.key}-policy"
    
    policy = data.aws_iam_policy_document.external_dns.json
}

resource "aws_iam_role_policy_attachment" "external_dns" {
    for_each = aws_iam_role.external_dns_role

    role = each.value.name
    policy_arn = aws_iam_policy.external_dns[each.key].arn
}

output "oidc_provider_arn" {
    value = aws_iam_openid_connect_provider.main.arn
}

output "external_dns_roles" {
    value = {
        for env in local.environments : env => {
            role_arn = aws_iam_role.external_dns_role[env].arn
            serviceaccount = local.env_config[env].serviceaccount
            domain_filters = local.env_config[env].domain_filters
        }
    }
}