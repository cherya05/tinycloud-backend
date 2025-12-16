locals {
    environments = ["dev", "staging", "prod"]

    env_config = {
        dev = {
            namespace = "tinycloud-dev"
            serviceaccount = "external-dns-dev"
            domain_filters = ["dev.hatstore-danil.info"]
        }
        staging = {
            namespace = "tinycloud-staging"
            serviceaccount = "external-dns-staging"
            domain_filters = ["staging.hatstore-danil.info"]
        }
        prod = {
            namespace = "tinycloud-prod"
            serviceaccount = "external-dns-prod"
            domain_filters = ["hatstore-danil.info"]
        }
    }
}