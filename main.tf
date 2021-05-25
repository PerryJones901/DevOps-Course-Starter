terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = ">= 2.49"
    }
  }
}

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "main" {
  name = "SoftwirePilot_PerryJones_ProjectExercise"
}

resource "azurerm_app_service_plan" "main" {
  name = "${var.prefix}-terraformed-asp"
  location = var.location
  resource_group_name = data.azurerm_resource_group.main.name
  kind = "Linux"
  reserved = true
  sku {
    tier = "Basic"
    size = "B1"
  }
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-ppp-perjon-cosmosdb-account"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  capabilities {
    name = "EnableMongo"
  }

  capabilities {
    name = "EnableServerless"
  }  

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 10
    max_staleness_prefix    = 200
  }

  geo_location {
    location          = data.azurerm_resource_group.main.location
    failover_priority = 0
  }
}

resource "azurerm_app_service" "main" {
  name = "${var.prefix}-perfect-productivity-platform"
  location = var.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id
  site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|perryjones/ppp:latest"
  }
  app_settings = {
   "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
   "MONGODB_CONNECTION_STRING" = "mongodb://${azurerm_cosmosdb_account.main.name}:${azurerm_cosmosdb_account.main.primary_key}@${azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "${var.prefix}-ppp-cosmos-mongo-db"
  resource_group_name = azurerm_cosmosdb_account.main.resource_group_name
  account_name        = azurerm_cosmosdb_account.main.name

  # lifecycle {
  #   prevent_destroy = true
  # }
}

