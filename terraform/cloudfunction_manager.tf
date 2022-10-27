resource "google_storage_bucket_object" "function_archive3" {
  name   = "schedule_manager_function.zip"
  bucket = google_storage_bucket.function_storage_bucket.name
  source = "../schedule_manager_function.zip"
}

resource "google_cloudfunctions_function" "function3" {
  name        = "schedule-manager-${terraform.workspace}"
  description = "Manages the whole processing of schedule"
  runtime     = "python39"

  source_archive_bucket = google_storage_bucket.function_storage_bucket.name
  source_archive_object = google_storage_bucket_object.function_archive3.name

  entry_point           = "entrypoint"

  event_trigger {
    event_type = "providers/cloud.pubsub/eventTypes/topic.publish"
    resource = google_pubsub_topic.manager_topic.name
  }

  environment_variables = {
    HOLEFINDER_TOPIC_NAME      = google_pubsub_topic.hole_finder.name
    GOOGLE_CLOUD_PROJECT = var.google_project_name
  }

  depends_on = [
    google_storage_bucket_object.function_archive3
  ]

}

