variable "prefix"{
    description = "The prefix used for all resources in this environment"
}
variable "flask_app"{
    description = "The location of flask app"
    sensitive   = true
}
variable "secret_key"{
    description = "Flask secret ket"
    sensitive   = true
}
variable "mongo_collection_name"{
    description = "The mongo collection name"
    sensitive   = true
}
variable "admin_id"{
    description = "The GitHub ID of the admin account"
    sensitive   = true
}
variable "oauth_client_id"{
    description = "GitHub oauth client_ID"
    sensitive   = true
}
variable "oauth_secret"{
    description = "GitHub oauth client_secret"
    sensitive   = true
}
