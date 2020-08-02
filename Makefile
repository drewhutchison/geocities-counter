deploy-test:
	gcloud functions deploy test-counter --entry-point test_counter \
	       --runtime python37 --trigger-http
deploy:
	gcloud functions deploy counter --entry-point get_counter \
	       --runtime python37 --trigger-http
