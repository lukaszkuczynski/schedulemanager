resource "google_pubsub_topic" "manager" {
  name                       = "manager-topic"
  message_retention_duration = "600s"
}

resource "google_pubsub_topic" "hole_finder" {
  name                       = "hole-finder-topic"
  message_retention_duration = "600s"
}

resource "google_pubsub_topic" "notifier" {
  name                       = "notifier-topic"
  message_retention_duration = "600s"
}

resource "google_pubsub_topic" "reader" {
  name                       = "reader-topic"
  message_retention_duration = "600s"
}
