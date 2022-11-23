variable "region" {
  default = "EUROPE-CENTRAL2"
}

variable "app_name" {
  default = "schedulemanager"
}

variable "google_project_name" {
}

variable "spreadsheet_id" {
}

variable "sheet_range" {
}
variable "twilio_account_sid" {
}
variable "twilio_auth_token" {
}
variable "notifier_from" {
}
variable "notifier_to" {
}
variable "days_ahead_check" {
  description = "How many days ahead manager is to check whether to send notifications about holes"
  default     = 7
}


variable "contact_data" {
  description = "contact data json (to be replaced soon)"
  default     = "{}"
}
