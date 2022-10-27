workspace := $(shell cd terraform && terraform workspace show)

echo:
	cd terraform && echo ${workspace}

package:
	rm -f *.zip 
	cd schedule_reader_function && zip -r ../schedule_reader_function.zip main.py requirements.txt
	cd hole_finder_function && zip -r ../hole_finder_function.zip main.py requirements.txt
	cd schedule_manager_function && zip -r ../schedule_manager_function.zip main.py requirements.txt


apply: package
	cd terraform && terraform apply -auto-approve -var-file="${workspace}.tfvars"

taint3:
	cd terraform && terraform taint google_cloudfunctions_function.function3
	
taint2:
	cd terraform && terraform taint google_cloudfunctions_function.function2

logs:
	gcloud functions logs read  schedule-reader-default --limit 10

state:
	cd terraform && terraform state list