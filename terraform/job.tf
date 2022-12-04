resource "google_cloud_scheduler_job" "job" {
  name        = "run_hole_finder"
  description = "Job that runs manager daily"
  schedule    = "15 21 * * 0,3"
  time_zone   = "Europe/Warsaw"


  pubsub_target {
    topic_name = google_pubsub_topic.reader.id
    data       = filebase64("hole_finder_config.json")
  }
}
