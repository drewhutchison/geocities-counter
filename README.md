Implementation of a super-dumb hit counter via Google Cloud Platform, described
at
https://ad0sk.net/building-a-geocities-style-hit-counter-with-google-cloud-functions.html.

You'll need [gcloud](https://cloud.google.com/sdk/gcloud/)
configured and pointing at a project with Cloud Functions and Firestore enabled.
Firestore should have a collection called `counter` set up through Cloud Console
or otherwise.

Then, `make deploy-test` will deploy the `test-counter` endpoint (which doesn't
need firestore), and `make deploy` will deploy `counter`.