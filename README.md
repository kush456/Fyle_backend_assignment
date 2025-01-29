## Running the application

### Build the docker image

Run the following command to build the Docker image: 

```
docker-compose build
```

### Start the service

Run the following command to start the services defined in the docker-compose.yml file:

```
docker-compose up
```
### Access the application

Open your browser and go to http://localhost:5000. You should see your Flask application running.

### Stop the Services:

To stop the services, press Ctrl+C in the terminal where you ran docker-compose up.

Alternatively, you can run the following command to stop the services:

```
docker-compose down
```


### Install requirements

```
virtualenv env --python=python3.8
source env/bin/activate
pip install -r requirements.txt
```
### Reset DB

```
export FLASK_APP=core/server.py
rm core/store.sqlite3
flask db upgrade -d core/migrations/
```
### Start Server

```
bash run.sh
```
### Run Tests

```
pytest -vvv -s tests/

# for test coverage report
# pytest --cov
# open htmlcov/index.html
```
