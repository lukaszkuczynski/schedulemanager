Google based Schedule Manager

basic functionalities:
- reads Google Sheet
- finds holes
- sends notifications

To read there is a IAM service account role required and given read permissions to Google Sheet

TODO:
- modularize functions in Terraform


start flow with sending this to the reader
{"message": {"data":"", "message":"", "flow":"SEND_TO_RECIPIENTS"}}