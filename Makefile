workspace := $(shell cd terraform && terraform workspace show)

echo:
	cd terraform && echo ${workspace}

package:
	rm -f *.zip 
	cd schedule_reader_function && zip -r ../schedule_reader_function.zip main.py sheet_shifts_parser.py requirements.txt
	cd hole_finder_function && zip -r ../hole_finder_function.zip main.py hole_detector.py requirements.txt
	cd schedule_manager_function && zip -r ../schedule_manager_function.zip main.py decisive.py requirements.txt
	cd notifier_function && zip -r ../notifier_function.zip main.py twilio_sender.py requirements.txt

apply: package
	cd terraform && terraform apply -auto-approve -var-file="${workspace}.tfvars"

taint:
	cd terraform && terraform taint module.cloudfunction_manager.google_cloudfunctions_function.function
	
logs:
	gcloud functions logs read  schedule-reader-default --limit 10 --start-time '2022-11-09' 

state:
	cd terraform && terraform state list

destroy:
	cd terraform && terraform destroy