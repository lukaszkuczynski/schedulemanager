
resource "google_storage_bucket_object" "function_archive2" {
  name   = "hole_finder_function.zip"
  bucket = google_storage_bucket.function_storage_bucket.name
  source = "../hole_finder_function.zip"
}

resource "google_cloudfunctions_function" "function2" {
  name        = "hole-finder-${terraform.workspace}"
  description = "Hole finder"
  runtime     = "python39"

  source_archive_bucket = google_storage_bucket.function_storage_bucket.name
  source_archive_object = google_storage_bucket_object.function_archive2.name
  entry_point           = "entrypoint"

  event_trigger {
    event_type = "providers/cloud.pubsub/eventTypes/topic.publish"
    resource = google_pubsub_topic.hole_finder.name
  }

  environment_variables = {
    MANAGER_TOPIC_NAME      = google_pubsub_topic.manager_topic.name
    GOOGLE_CLOUD_PROJECT = var.google_project_name
  }

  depends_on = [
    google_storage_bucket_object.function_archive2
  ]

}
