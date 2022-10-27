resource "google_pubsub_topic" "manager_topic" {
  name = "manager-topic"
  message_retention_duration = "86600s"
}

resource "google_pubsub_topic" "hole_finder" {
  name = "hole-finder-topic"
  message_retention_duration = "86600s"
}