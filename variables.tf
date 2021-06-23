variable "prefix" {
  description = "The prefix used for all resources in this environment"
}

variable "location" {
  description = "The Azure location where all resources in this deployment should be created"
  default = "uksouth"
}

variable "auth_client_id" {
  description = "Client Id for GitHub Auth"
}

variable "auth_client_secret" {
  description = "Client Secret for GitHub Auth"
}

variable "log_level" {
  description = "The level of log severity (e.g. DEBUG, INFO, ERROR etc)"
}

variable "loggly_token" {
  description = "Token for Loggly"
}

variable "mongo_db_name" {
  description = "Name of MongoDB database the app will connect to"
}

variable "secret_key" {
  description = "Secret Key which is given to Flask as SECRET_KEY"
}