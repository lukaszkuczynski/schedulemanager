Google based Schedule Manager

basic functionalities:
- reads Google Sheet
- finds holes
- sends notifications

To read there is a IAM service account role required and given read permissions to Google Sheet




start flow with sending this to the reader
{"data": {"message":"", "flow":"SEND_TO_RECIPIENTS", "caller": "manual"}, "messageType": "json"}