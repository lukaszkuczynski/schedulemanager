resource "google_cloud_scheduler_job" "job" {
  name        = "read_spreadsheet_daily"
  description = "Job that runs manager daily"
  schedule    = "0 22 * * *"
  time_zone   = "Europe/Warsaw"


  pubsub_target {
    topic_name = google_pubsub_topic.reader.id
    data       = base64encode("test")
  }
}
