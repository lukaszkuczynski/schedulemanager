workspace := $(shell cd terraform && terraform workspace show)

echo:
	cd terraform && echo ${workspace}

package:
	rm -f *.zip 
	cd schedule_reader_function && zip -r ../schedule_reader_function.zip main.py requirements.txt

apply: package
	cd terraform && terraform apply -auto-approve -var-file="${workspace}.tfvars"

taint:
	cd terraform && terraform taint google_cloudfunctions_function.schedule_reader_function

logs:
	gcloud functions logs read  schedule-reader-default --limit 10
