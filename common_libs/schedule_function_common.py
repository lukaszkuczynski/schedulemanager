import os
import json
import base64
from google.cloud import pubsub_v1


def get_required_env_var(varname, default=None):
    env_value = os.getenv(varname, default)
    if env_value is None:
        raise Exception(f"Required env var {varname} is not defined. Aborting!")
    return env_value


class CommsHelper:
    def __init__(self, project_id, this_caller_id, manager_topic=None) -> None:
        self.__publisher = pubsub_v1.PublisherClient()
        self.__project_id = project_id
        self.__manager_topic = manager_topic
        self.__this_caller_id = this_caller_id

    def parse_the_response(self, event):
        print(f"Received event with ID: {event['id']} and data {event.data}")
        if "messageType" in event.data["message"]:
            if event.data["message"]["messageType"] == "json":
                data_parsed = event.data["message"]
        else:
            data_parsed = json.loads(
                base64.b64decode(event.data["message"]["data"]).decode()
            )
        print(data_parsed)
        data = data_parsed.get("data")
        message = data.get("message")
        caller = data.get("caller")
        flow = data.get("flow")
        return caller, message, flow

    def call_the_manager(self, flow, response):
        topic_path = self.__publisher.topic_path(
            self.__project_id, self.__manager_topic
        )
        message_json = json.dumps(
            {
                "data": {
                    "message": response,
                    "caller": self.__this_caller_id,
                    "flow": flow,
                }
            }
        )
        message_bytes = message_json.encode("utf-8")
        try:
            publish_future = self.__publisher.publish(topic_path, data=message_bytes)
            return publish_future.result()
        except Exception as e:
            print(e)
            return (e, 500)

    def send_to_topic(self, topic_name, flow, response):
        topic_path = self.__publisher.topic_path(self.__project_id, topic_name)
        message_json = json.dumps(
            {
                "data": {
                    "message": response,
                    "caller": self.__this_caller_id,
                    "flow": flow,
                }
            }
        )
        message_bytes = message_json.encode("utf-8")
        try:
            publish_future = self.__publisher.publish(topic_path, data=message_bytes)
            publish_result = publish_future.result()  # Verify the publish succeeded
            print(publish_result)
            return "Message published."
        except Exception as e:
            print(e)
            return (e, 500)
