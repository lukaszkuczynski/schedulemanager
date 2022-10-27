import functions_framework
import base64

@functions_framework.cloud_event
def entrypoint(schedule_cloud_event):
   print(f"Received event with ID: {schedule_cloud_event['id']} and data {schedule_cloud_event.data}")
   print("decoding")
   decoded = base64.b64decode(schedule_cloud_event.data["message"]["data"]).decode()
   print("Hello, " + decoded + "!")
   print(decoded)
