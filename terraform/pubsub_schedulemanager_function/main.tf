
resource "google_storage_bucket_object" "function_archive" {
  name   = var.archive_file_name
  bucket = var.function_storage_bucket
  source = "../hole_finder_function.zip"
}

resource "google_cloudfunctions_function" "function" {
  name    = var.function_name
  runtime = "python39"

  source_archive_bucket = var.function_storage_bucket
  source_archive_object = google_storage_bucket_object.function_archive.name
  entry_point           = var.entrypoint


  event_trigger {
    event_type = "providers/cloud.pubsub/eventTypes/topic.publish"
    resource   = var.trigger_pubsub_topic
  }

  environment_variables = {
    MANAGER_TOPIC_NAME   = var.manager_topic_name
    GOOGLE_CLOUD_PROJECT = var.google_project_name
  }

  depends_on = [
    google_storage_bucket_object.function_archive
  ]

}
