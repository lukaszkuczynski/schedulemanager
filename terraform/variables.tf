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

variable "dry_run_send" {
  default = 1
}

variable "hole_notified_people" {
  description = "comma separated list of names notified about holes"
  default     = ""
}

variable "ics_event_name" {
  description = "Event to be identified when creating ICS file for a shift in shift_recorder function"
  default     = ""
}

variable "ics_organizer_email" {
  description = "Event's organizer to be identified when creating ICS file for a shift in shift_recorder function"
  default     = ""
}

variable "ics_storage_bucket" {
  description = "Cloud Storage bucket name to store all ICS files for shifts"
  default     = ""
}

