# RecsByText

Recommend movies to your friends and ask them for recommendations all through a convenient SMS interface.

[![Build Status](https://travis-ci.org/karllhughes/recs-by-text.svg?branch=master)](https://travis-ci.org/karllhughes/recs-by-text)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You should have the following installed on your local machine:

- Python 3.X with pip
- Postgres 11.X
- [ngrok](https://ngrok.com/)

This app uses [Twilio](https://www.twilio.com/) to send and receive messages, so you will need an account, phone number, and API key.

### Running Locally

- Make sure Postgres is running and a database is created using the credentials in `./moviesByPhone/settings.py`.
- Clone this repository and navigate to the directory:

```bash
git clone karllhughes/movies-by-phone
cd movies-by-phone
```

- Set up a virtual environment: `python -m venv venv`
- Install dependencies with pip: `pip install -r requirements.txt`
- Sync and migrate the database:

```bash
python ./manage.py syncdata
python ./manage.py migrate
```

- (Optional) Create a superuser for your admin panel: `python ./manage.py createsuperuser`
- Run the server: `python ./manage.py runserver`

The app will now be running, and you can check out the landing page at [localhost:8000](http://localhost:8000/).

#### Importing Movies

You can import movies from the IMDB [data dump found here](https://datasets.imdbws.com/). This data is used to recommend new
movies to users based on their existing list.

- Download and unzip the `title.basics.tsv` and `title.crew.tsv` files
- Copy them into the `moviesImporter/data_to_import` directory
- Run the import script: `python ./manage.py runscript importer`

You should see a summary of the number of movies imported and the time taken (~2 minutes).

### Running Locally with Docker

- Clone the repository and navigate to the directory (see above)
- Run a Postgres database: `docker run --rm --name pg -e POSTGRES_PASSWORD='' -e POSTGRES_USER='postgres' -e POSTGRES_DB='moviesByPhone' -p 5432:5432 -d postgres:11`
- Build the web app Docker Image: `docker build -t recs-by-text .`
- Run the container: `docker run --rm -d -v $(pwd)/recommendations:/app/recommendations -p 8000:8000 --link=pg --name web recs-by-text`

The first time, you'll need to run the migrations:

```bash
docker exec -it web python ./manage.py syncdata
docker exec -it web python ./manage.py migrate
```

## Running the tests

Run the tests with `python ./manage.py test`.

### And coding style tests

Test for style inconsistencies with `pycodestyle recommendations`

## Contributing

Contributions are welcome! Please create an issue first to solicit discussion, then make a pull request with your improvements.

## Authors

- [Josh Alletto](https://github.com/jalletto)
- [Karl Hughes](https://github.com/karllhughes)

See also the list of [contributors](https://github.com/karllhughes/movies-by-phone/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
