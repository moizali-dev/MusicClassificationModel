# Music Classification

The purpose of this project is to create a model which will predict the genre of a track `'Hip-Hop':0, 'Pop':1, 'Country':2, 'Rock':3, 'R&B':4, 'Dance/Electronic':5, 'Indie':6, 'Sleep':7, 'Jazz':8, 'Soul':9, 'Metal':10` based on the 13 audio features provided from the Spotify API

# Demo

https://user-images.githubusercontent.com/22460824/210695071-160a033e-fbe9-410d-ad63-0dacfeb42b01.mov

## Background

Music classification has a wide range of uses from tagging new songs that were uploaded and profiling them automatically at scale to figuring out which genre a user listens to more and possibly having it as an input for a recommendation system

## Data Ingestion

The dataset is created using the Spotify API. It downloads all the tracks from a playlist as `Tracks` object and for each track gets the features.

Each playlist is tagged a genre based on the name of the playlist

There are 13 audio features for each track, including confidence measures like `acousticness`, `liveness`, `speechiness` and `instrumentalness`, perceptual measures like `energy`, `loudness`, `danceability` and `valence` (positiveness), and descriptors like `duration`, `tempo`, `key`, `time signature` and `mode`.

The data is fetched from the analytics zone of big query dataset. Currently the model was built on `37015` tracks

## Modelling

### Data Cleaning

- The Target variable was created based on the genre
- Data was cleaned to make sure there were not any NAs
- Duplicate tracks were removed (since more than one playlist can have the same track)
- Remove columns that were not required for modelling such as `type`,`id`,`uri`,`track_href`,`analysis_url` etc.

### Model Training

An `Xgboost` algorithm was used to predict the target variable

Grid search methodology was used for hyperparameter tuning. The optimal parameters came out to be:

```
{'max_depth': 100, 'max_features': 2, 'min_samples_leaf': 3, 'min_samples_split': 8, 'n_estimators': 100}
```

### Model Performance

## Deployment of the model

### Local Deployment

The model can be deployed locally using Docker and the following commands

```
docker build -t musicpred .
docker run -it --rm -p 9698:9698 musicpred
```

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
