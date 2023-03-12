workspace := $(shell cd terraform && terraform workspace show)

echo:
	cd terraform && echo ${workspace}

package:
	rm -f *.zip 
	cp common_libs/schedule_function_common.py schedule_reader_function/
	cp common_libs/schedule_function_common.py hole_finder_function/
	cp common_libs/schedule_function_common.py schedule_manager_function/
	cp common_libs/schedule_function_common.py notifier_function/
	cd schedule_reader_function && zip -r ../schedule_reader_function.zip main.py sheet_shifts_parser.py requirements.txt schedule_function_common.py 
	cd hole_finder_function && zip -r ../hole_finder_function.zip main.py hole_detector.py requirements.txt schedule_function_common.py 
	cd schedule_manager_function && zip -r ../schedule_manager_function.zip main.py decisive.py contacts_helper.py requirements.txt schedule_function_common.py 
	cd notifier_function && zip -r ../notifier_function.zip main.py twilio_sender.py requirements.txt schedule_function_common.py
	cd shift_recorder_function && zip -r ../shift_recorder_function.zip main.py shift_saver.py requirements.txt schedule_function_common.py

apply: package
	cd terraform && terraform apply -auto-approve -var-file="${workspace}.tfvars"

taint:
	# cd terraform && terraform taint module.cloudfunction_manager.google_cloudfunctions_function.function
	# cd terraform && terraform taint module.cloudfunction_reader.google_cloudfunctions_function.function
	# cd terraform && terraform taint module.cloudfunction_finder.google_cloudfunctions_function.function
	# cd terraform && terraform taint module.cloudfunction_notifier.google_cloudfunctions_function.function
	cd terraform && terraform taint module.cloudfunction_shiftrecorder.google_cloudfunctions_function.function
	
logs:
	gcloud functions logs read  schedule-reader-default --limit 10 --start-time '2022-11-09' 

state:
	cd terraform && terraform state list

destroy:
	cd terraform && terraform destroy