variable "archive_file_name" {
  description = "Stores archive file name with ZIP containing the function itself"
}

variable "function_name" {
  description = "name of CloudFunction"
}

variable "entrypoint" {
  description = "entrypoint of a CloudFunction"
  default     = "entrypoint"
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

variable "additional_variables" {
  description = "map holding additional env variables for a Function"
}

variable "available_memory_mb" {
  description = "How much memory is available for the Function"
  default     = 256
}

variable "spreadsheet_id" {
  description = "Google Sheets spreadsheet id to read schedule by a reader"
  default     = ""
}

variable "sheet_range" {
  description = "Sheet range of a Google Sheet with the schedule"
  default     = ""
}
