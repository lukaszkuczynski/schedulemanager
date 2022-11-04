resource "google_storage_bucket" "function_storage_bucket" {
  name     = "${var.app_name}-${terraform.workspace}"
  location = var.region
}

resource "google_storage_bucket_object" "schedule_reader_archive" {
  name   = "schedule_reader_function.zip"
  bucket = google_storage_bucket.function_storage_bucket.name
  source = "../schedule_reader_function.zip"
}

resource "google_cloudfunctions_function" "schedule_reader_function" {
  name        = "schedule-reader-${terraform.workspace}"
  description = "Schedule reading function"
  runtime     = "python39"

  available_memory_mb   = 512
  source_archive_bucket = google_storage_bucket.function_storage_bucket.name
  source_archive_object = google_storage_bucket_object.schedule_reader_archive.name
  trigger_http          = true
  entry_point           = "entrypoint"

  depends_on = [
    google_storage_bucket_object.schedule_reader_archive
  ]

  environment_variables = {
    SPREADSHEET_ID       = var.spreadsheet_id
    SHEET_RANGE          = var.sheet_range
    MANAGER_TOPIC_NAME   = google_pubsub_topic.manager_topic.name
    GOOGLE_CLOUD_PROJECT = var.google_project_name
  }
}

# IAM entry for all users to invoke the function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.schedule_reader_function.project
  region         = google_cloudfunctions_function.schedule_reader_function.region
  cloud_function = google_cloudfunctions_function.schedule_reader_function.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}
