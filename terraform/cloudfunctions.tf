module "cloudfunction_notifier" {
  source = "./pubsub_schedulemanager_function"

  archive_file_name       = "./notifier_function.zip"
  function_name           = "notifier-${terraform.workspace}"
  entrypoint              = "entrypoint"
  trigger_pubsub_topic    = google_pubsub_topic.notifier.name
  function_storage_bucket = google_storage_bucket.function_storage_bucket.name
  manager_topic_name      = google_pubsub_topic.manager_topic.name
  google_project_name     = var.google_project_name

  additional_variables = {
    MANAGER_TOPIC_NAME   = google_pubsub_topic.manager_topic.name
    GOOGLE_CLOUD_PROJECT = var.google_project_name
  }
}

module "cloudfunction_manager" {
  source = "./pubsub_schedulemanager_function"

  archive_file_name       = "./schedule_manager_function.zip"
  function_name           = "schedule-manager-${terraform.workspace}"
  entrypoint              = "entrypoint"
  trigger_pubsub_topic    = google_pubsub_topic.manager_topic.name
  function_storage_bucket = google_storage_bucket.function_storage_bucket.name
  manager_topic_name      = google_pubsub_topic.manager_topic.name
  google_project_name     = var.google_project_name

  additional_variables = {
    HOLEFINDER_TOPIC_NAME = google_pubsub_topic.hole_finder.name
    MANAGER_TOPIC_NAME    = google_pubsub_topic.manager_topic.name
    GOOGLE_CLOUD_PROJECT  = var.google_project_name
  }
}

