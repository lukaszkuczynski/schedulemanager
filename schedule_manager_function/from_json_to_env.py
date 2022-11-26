# very basic tool that creates ENVVAR with json to be put
# temporary solution to store contacts data

import json
import os
import re

CONTACT_FILE_PATH = os.path.expanduser("~/.contacts.json")
ENV_KEY_NAME = "contact_data"
ENV_FILENAME = "../terraform/prod.tfvars"
print(CONTACT_FILE_PATH)


with open(CONTACT_FILE_PATH) as fread:
    contacts = json.load(fread)
    new_env_text = ""
    with open(ENV_FILENAME) as fenv:
        env_file_content = fenv.read()
        flat_contacts_json = json.dumps(contacts, ensure_ascii=False).replace(
            '"', '\\"'
        )
        new_env_text = re.sub(
            r"contact_data\s+=\s+(.+)",
            f'contact_data = "{flat_contacts_json}"',
            env_file_content,
        )
    if new_env_text:
        print("Writing new file content!")
        print(new_env_text)
        with open(ENV_FILENAME, "w") as fenv:
            fenv.write(new_env_text)
