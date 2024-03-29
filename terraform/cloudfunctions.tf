resource "google_storage_bucket" "function_storage_bucket" {
  name     = "${var.app_name}-${terraform.workspace}"
  location = var.region
}

module "cloudfunction_notifier" {
  source = "./pubsub_schedulemanager_function"

  archive_file_name       = "./notifier_function.zip"
  function_name           = "notifier-${terraform.workspace}"
  trigger_pubsub_topic    = google_pubsub_topic.notifier.name
  function_storage_bucket = google_storage_bucket.function_storage_bucket.name
  manager_topic_name      = google_pubsub_topic.manager.name
  google_project_name     = var.google_project_name

  additional_variables = {
    MANAGER_TOPIC_NAME   = google_pubsub_topic.manager.name
    GOOGLE_CLOUD_PROJECT = var.google_project_name
    TWILIO_ACCOUNT_SID   = var.twilio_account_sid
    TWILIO_AUTH_TOKEN    = var.twilio_auth_token
    NOTIFIER_FROM        = var.notifier_from
    NOTIFIER_TO          = var.notifier_to
    DRY_RUN_SEND         = var.dry_run_send
  }
}

module "cloudfunction_manager" {
  source = "./pubsub_schedulemanager_function"

  archive_file_name       = "./schedule_manager_function.zip"
  function_name           = "schedule-manager-${terraform.workspace}"
  trigger_pubsub_topic    = google_pubsub_topic.manager.name
  function_storage_bucket = google_storage_bucket.function_storage_bucket.name
  manager_topic_name      = google_pubsub_topic.manager.name
  google_project_name     = var.google_project_name

  additional_variables = {
    HOLEFINDER_TOPIC_NAME     = google_pubsub_topic.hole_finder.name
    MANAGER_TOPIC_NAME        = google_pubsub_topic.manager.name
    GOOGLE_CLOUD_PROJECT      = var.google_project_name
    NOTIFIER_TOPIC_NAME       = google_pubsub_topic.notifier.name
    DAYS_AHEAD_CHECK          = var.days_ahead_check
    CONTACT_DATA              = var.contact_data
    HOLE_NOTIFIED_PEOPLE      = var.hole_notified_people
    SHIFT_RECORDER_TOPIC_NAME = google_pubsub_topic.shift_recorder.name
  }
}

module "cloudfunction_finder" {
  source = "./pubsub_schedulemanager_function"

  archive_file_name       = "./hole_finder_function.zip"
  function_name           = "hole-finder-${terraform.workspace}"
  trigger_pubsub_topic    = google_pubsub_topic.hole_finder.name
  function_storage_bucket = google_storage_bucket.function_storage_bucket.name
  manager_topic_name      = google_pubsub_topic.manager.name
  google_project_name     = var.google_project_name

  additional_variables = {
    MANAGER_TOPIC_NAME   = google_pubsub_topic.manager.name
    GOOGLE_CLOUD_PROJECT = var.google_project_name
  }
}

module "cloudfunction_reader" {
  source = "./pubsub_schedulemanager_function"

  archive_file_name       = "./schedule_reader_function.zip"
  function_name           = "schedule-reader-${terraform.workspace}"
  trigger_pubsub_topic    = google_pubsub_topic.reader.name
  function_storage_bucket = google_storage_bucket.function_storage_bucket.name
  manager_topic_name      = google_pubsub_topic.manager.name
  google_project_name     = var.google_project_name
  available_memory_mb     = 512

  additional_variables = {
    MANAGER_TOPIC_NAME   = google_pubsub_topic.manager.name
    GOOGLE_CLOUD_PROJECT = var.google_project_name
    SPREADSHEET_ID       = var.spreadsheet_id
    SHEET_RANGE          = var.sheet_range
  }
}

module "cloudfunction_shiftrecorder" {
  source = "./pubsub_schedulemanager_function"

  archive_file_name       = "./shift_recorder_function.zip"
  function_name           = "shift-recorder-${terraform.workspace}"
  trigger_pubsub_topic    = google_pubsub_topic.shift_recorder.name
  function_storage_bucket = google_storage_bucket.function_storage_bucket.name
  manager_topic_name      = google_pubsub_topic.manager.name
  google_project_name     = var.google_project_name

  additional_variables = {
    MANAGER_TOPIC_NAME   = google_pubsub_topic.manager.name
    GOOGLE_CLOUD_PROJECT = var.google_project_name
    ICS_EVENT_NAME       = var.ics_event_name
    ICS_ORGANIZER_EMAIL  = var.ics_organizer_email
    ICS_STORAGE_BUCKET   = var.ics_storage_bucket
  }
}

