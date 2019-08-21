# RecsByText

Recommend movies to your friends and ask them for recommendations all through a convenient SMS interface.

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

Coming soon!

## Contributing

Contributions are welcome! Please create an issue first to solicit discussion, then make a pull request with your improvements.

## Authors

- [Josh Alletto](https://github.com/jalletto)
- [Karl Hughes](https://github.com/karllhughes)

See also the list of [contributors](https://github.com/karllhughes/movies-by-phone/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
