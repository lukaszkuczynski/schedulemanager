variable "archive_file_name" {
  description = "Stores archive file name with ZIP containing the function itself"
}

variable "function_name" {
  description = "name of CloudFunction"
}

variable "entrypoint" {
  description = "entrypoint of a CloudFunction"
}

variable "trigger_pubsub_topic" {
  description = "name of a PubSub topic to trigger this Function"
}

variable "function_storage_bucket" {
  description = "Bucket to store archives of Cloud Function(s)"
}

variable "manager_topic_name" {
  description = "Topic to return results of this Function's execution via PubSub"
}

variable "google_project_name" {
  description = "project name (maybe to remove later with DataSource)"
}
