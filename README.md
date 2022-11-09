# Music Classification

The purpose of this project is to create a model which will predict the genre of a track based on the attributes such as loudness, energy, acoustic etc.

## Background

## Data Ingestion

## Modelling

## Deployment of the model

### Local Deployment




### Cloud Deployment (GCP)

1. Create a project and enable `cloud build` and `cloud run` api
2. Add below code to docker file at the end
```
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 predict:app
```
3. Change directory to where the Docker file resides i.e. 03_model_deployment/ and run the below commands

```
gcloud builds submit --tag gcr.io/{project_id}/predict
gcloud run deploy --image gcr.io/{project_id}/predict --platform managed
```
4. Change the url in the `predict_test.py` file to `{url from google cloud run}/predict` and run the script to get the prediction
