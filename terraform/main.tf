terraform {
    required_providers {
        azurerm = {
            source = "hashicorp/azurerm"
            version = ">= 3.8"
        }
    }
    backend "azurerm" {
        resource_group_name  = "LV21_PhilipWilson_ProjectExercise"
        storage_account_name = "tfstatephilapps"
        container_name       = "tfstate"
        key                  = "terraform.tfstate"
    }
}

provider "azurerm" {
    features {}
}

data "azurerm_resource_group" "main" {
    name = "LV21_PhilipWilson_ProjectExercise"
}

resource "azurerm_service_plan" "main" {
    name                    = "${var.prefix}-terraformed-asp"
    location                = data.azurerm_resource_group.main.location
    resource_group_name     = data.azurerm_resource_group.main.name
    os_type                 = "Linux"
    sku_name                = "B1"
}

resource "azurerm_linux_web_app" "main" {
    name                    = "${var.prefix}-todo-terraformed"
    location                = data.azurerm_resource_group.main.location
    resource_group_name     = data.azurerm_resource_group.main.name
    service_plan_id         = azurerm_service_plan.main.id

    site_config {
        application_stack {
            docker_image        = "philw10/todo-app"
            docker_image_tag    = "latest"   
        }
    }

    app_settings = {
        "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
        "MONGODB_CONNECTION_STRING"  = azurerm_cosmosdb_account.main.connection_strings[0]
        "FLASK_APP"                  = var.flask_app
        "SECRET_KEY"                 = var.secret_key
        "MONGO_DATABASE_NAME"        = azurerm_cosmosdb_mongo_database.main.name
        "MONGO_COLLECTION_NAME"      = var.mongo_collection_name
        "ADMIN_ID"                   = var.admin_id
        "GITHUB_OAUTH_CLIENT_ID"     = var.oauth_client_id
        "GITHUB_OAUTH_SECRET"        = var.oauth_secret
    }
}

resource "azurerm_cosmosdb_account" "main" {
    name     = "${var.prefix}-mongodb-account-terraformed"
    location                = data.azurerm_resource_group.main.location
    resource_group_name     = data.azurerm_resource_group.main.name
    offer_type              = "Standard"
    kind                    = "MongoDB"

    enable_automatic_failover = false

    capabilities {
        name = "EnableServerless"
    }

    capabilities {
        name = "EnableMongo"
    }

    lifecycle {
        prevent_destroy = false
    }

    consistency_policy {
        consistency_level           = "Session"
        max_interval_in_seconds     = 5
        max_staleness_prefix        = 100
    }

    geo_location {
        location            = "UK South"
        failover_priority   = 0
    }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
    name                    = "${var.prefix}-todo_app_mongodb_terraform"
    resource_group_name     = data.azurerm_resource_group.main.name
    account_name            = azurerm_cosmosdb_account.main.name
}