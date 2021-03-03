# Capstone Project

This project for Udacity's Full Stack Nanodegree Program using the Casting Agency specifications.

This is an API hosted on https://capstone-udacity-boren.herokuapp.com/.

## Casting Agency
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

### Models:
- Movies with attributes title and release date
- Actors with attributes name, age and gender
### Endpoints:
Responses and request bodies (for endpoints that require them) are all in JSON.
- GET `'/actors'`
  - Return an array of all actors
  - Requires the `view:actors` permission, available to the roles: casting assistant, casting director,
    executive producer
  - Example response:
    ```json
    [
      {
        "id": 1,
        "name": "David",
        "age": 36,
        "gender": "M"
      },
      {
        "id": 2,
        "name": "Alice",
        "age": 56,
        "gender": "F"
      }
    ]
    ```
- GET `'/movies'`
  - Return an array of all actors
  - `release_date` is in the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Dates) format, i.e. YYYY-MM-DD with 0 padding for the month and day.
  - Requires the `view:movies` permission, available to the roles: casting assistant, casting director,
    executive producer
  - Example response:
    ```json
    [
      {
        "id": 1,
        "title": "Movie A",
        "release_date": "2021-01-01"
      },
      {
        "id": 2,
        "title": "Movie B",
        "release_date": "1995-12-20"
      }
    ]
    ```
- POST `'/actors'`
  - Create a new actor
  - Request arguments:\
    `name`: Name of the actor.\
    `age`: Age of the actor. Must be a positive integer.\
    `gender`: Gender of the actor. Optional.
  - Return an object with the `id` of the newly created actor
  - Requires the `add:actor` permission, available to the roles: casting director, executive producer
  - Example request:
    ```json
    {
      "name": "John",
      "age": 43,
      "gender": "M"
    }
    ```
  - Example response:
    ```json
    {
      "id": 2
    }
    ```
- POST `'/movies'`
  - Create a new movie
  - Request arguments:\
    `title`: Title of the movie.\
    `release_date`: Release date of the movie. Must be a string in
    [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Dates) format, i.e. YYYY-MM-DD with 0 padding for
    the month and day.
  - Return an object with the `id` of the newly created movie
  - Requires the `add:movie` permission, available to the role: executive producer
  - Example request:
    ```json
    {
      "title": "Titanic",
      "release_date": "1997-12-19"
    }
    ```
  - Example response:
    ```json
    {
      "id": 3
    }
    ```
- PATCH `'/actors/<actor-id>'`
  - Update at least one attribute of the actor with the id `<actor-id>`: name, age or gender.
  - Request arguments:\
    At least one of\
    `name`: Name of the actor.\
    `age`: Age of the actor. Must be a positive integer.\
    `gender`: Gender of the actor.
  - Return the updated actor with members: `id`, `name`, `age`, `gender`.
  - Requires the `update:actor` permission, available to the roles: casting director, executive producer
  - Example request:
    ```json
    {
      "name": "New Name"
    }
    ```
  - Example response:
    ```json
    {
      "id": 2,
      "name": "New Name",
      "age": 43,
      "gender": "M"
    }
    ```
- PATCH `'/movies/<movie-id>'`
  - Update at least one attribute of the movie with the id `<movie-id>`: title or release_date.
  - Request arguments:\
    At least one of\
    `title`: Title of the movie.\
    `release_date`: Release date of the movie. Must be a string in
    [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Dates) format, i.e. YYYY-MM-DD with 0 padding for
    the month and day.
  - Return the updated movie with members: `id`, `title`, `release_date`.
  - Requires the `update:movie` permission, available to the roles: casting director, executive producer
  - Example request:
    ```json
    {
      "date": "2030-06-06"
    }
    ```
  - Example response:
    ```json
    {
      "id": 3,
      "title": "Titanic",
      "release_date": "2030-06-06"
    }
    ```
- DELETE `'/actors/<actor-id>'`
  - Delete an actor with the id `<actor-id>`.
  - Return a JSON object with the id of the deleted actor.
  - Requires the `delete:actor` permission, available to the roles: casting director, executive producer
  - Example response:
    ```json
    {
      "id": 2
    }
    ```
- DELETE `'/movies/<movie-id>'`
  - Delete a movie with the id `<movie-id>`.
  - Return a JSON object with the id of the deleted movie.
  - Requires the `delete:movie` permission, available to the role: executive producer
  - Example response:
    ```json
    {
      "id": 3
    }
    ```

### Errors:
HTTP errors return a JSON object corresponding to the status codes.
- 400 - Bad request
  ```json
  {
    "error": 400,
    "message": "bad request"
  }
  ```
- 401 - Unauthorized
  ```json
  {
    "error": 401,
    "message": "specific error message"
  }
  ```
- 403 - Forbidden
  ```json
  {
    "error": 403,
    "message": "specific error message"
  }
  ```
- 404 - Not found
  ```json
  {
    "error": 404,
    "message": "not found"
  }
  ```
- 405 - Method not allowed
  ```json
  {
    "error": 405,
    "message": "method not allowed"
  }
  ```
- 422 - Unprocessable
  ```json
  {
    "error": 422,
    "message": "unprocessable"
  }
  ```
- 500 - Internal server error
  ```json
  {
    "error": 500,
    "message": "Internal server error"
  }
  ```

### Roles:
- Casting Assistant
  - Can view actors and movies
- Casting Director
  - All permissions a Casting Assistant has and…
  - Add or delete an actor from the database
  - Modify actors or movies
- Executive Producer
  - All permissions a Casting Director has and…
  - Add or delete a movie from the database

### Authorization
This API uses [Auth0](https://auth0.com/) for authorization.

For all endpoints, authorization is needed for a successful response, or it will return a 401 unauthorized response.
This is done by adding an authorization header with a bearer token including a JWT in each request.

Example:
```
curl --request GET \
  --url http://localhost:5000/actors \
  --header 'authorization: Bearer YOUR_ACCESS_TOKEN'
```

The following JWTs are valid for the corresponding roles until 2021/03/12. Contact the developer for updated JWTs.
#### Casting assistant
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ijh4WmkwQTJDS205bmdrZmVwb21xZCJ9.eyJpc3MiOiJodHRwczovL2JvcmVueC5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzZGE1MTBiYWZiM2YwMDY5YTFkZDRlIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTQ2NTg0NDgsImV4cCI6MTYxNTUyMjQ0OCwiYXpwIjoiN2FqT2RhZ0NuelJQbTlSa0lWcFpzbkJvbGlBdHhlaVYiLCJwZXJtaXNzaW9ucyI6WyJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.xuLgZztDOkE13mRelsF98JfgLPBu0PCFevU3hMooAA2YnjFuDOrPlb7UlMnpWWIJ6EniagGluBmyPYHe6IB-IBvhI2Cpbdkyd0vox8pqzFk2twgcQP0EgvvrzJsdyU-E0B2o9ctTIdbStEylv7fBrl758T08P0AtiE1uHG5qXSeAHVzXmk6hD78XMyIb5jt_AmCRVvLYNF0Y82LO8M64_3vcXf1P11PmcEuq1i6h3ZT7SiozSrvLUeYNmvWewFf9ikK5kTSxdcoZzyNg1P-Roz-QVmynTRVWGG5yFYmbR4ipI5MHrpZ_7qPIi3DOunxKyChgHq77JlaexchvX2lpCg
#### Casting director
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ijh4WmkwQTJDS205bmdrZmVwb21xZCJ9.eyJpc3MiOiJodHRwczovL2JvcmVueC5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAxY2IyNzc0MWRiOGUwMDcwNmYxMGFkIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTQ2NTkwMTAsImV4cCI6MTYxNTUyMzAxMCwiYXpwIjoiN2FqT2RhZ0NuelJQbTlSa0lWcFpzbkJvbGlBdHhlaVYiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWN0b3IiLCJkZWxldGU6YWN0b3IiLCJ1cGRhdGU6YWN0b3IiLCJ1cGRhdGU6bW92aWUiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.sRA6TObo5Iv9LOEnxWoAEa5KHQfMPAvyj4X6hyXpGOnrHq5ss59Qd8g5EnFbFyzPclsq13O7s-QU8ROsq7fxybNzNrMEdzjqZilE8lrZ6i0lB4p-KV35Nv-CYyDqsxACSkLQXa_hXGQgVZgLgfskWFr_PJrCXwiQFlDIh4_eKNxqhm69cYIBaen0OESLK4L0Lcl_uOQYFmSmZX98D441yiAX7mVAZPj-Tz5m6v97_gr292Ee5omg6C0xI1DUhW3_usC7jargrhuUXeB41Y83lXlky0K1Jghee8OojJc8xr6HyzZENb7PfzM0oMXA1M0VSeP548RHZKhlPFhqxHE9XA
#### Executive producer
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ijh4WmkwQTJDS205bmdrZmVwb21xZCJ9.eyJpc3MiOiJodHRwczovL2JvcmVueC5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAxY2IzNjM5YWNiYzIwMDZhYjhlZjY2IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTQ2NTg4NTEsImV4cCI6MTYxNTUyMjg1MSwiYXpwIjoiN2FqT2RhZ0NuelJQbTlSa0lWcFpzbkJvbGlBdHhlaVYiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWN0b3IiLCJhZGQ6bW92aWUiLCJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJ1cGRhdGU6YWN0b3IiLCJ1cGRhdGU6bW92aWUiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.aGyZjGeUG5xxnTEFIhyT8T4EetA0IqPdje6HpX3f5rxJesDdMzUN-kD8nFsEBe3YEnlo8vyetDY_popx5Ny7MSvi036Y--IsyTQwxVLrxhS-OdyUGxkfPfapIpk6IWw4MpGfb1wWFGZDxO0Arxq82G0cFeLdxhTacoKmlY8VlrSuIMe3iaQxQyOmhQJbJJvJwm6Hil9UI3QAYkLunQf5bbrCOXZpLRHWbdSGYl54o-RC7y82LTGRKGh-FEYnDjbjUml5wfD0RIXCbUDZCx_Vpgcq-AUIlI58S6IUnXguRw5ZZ32cfWcCVmopTIqgitd_FjDeNO6Fi3nqzIfI0KJDVg

### How to run on your environment
This app requirements Python 3.7+ to run.
- Install the python dependencies by running `pip install -r requirements.txt`, optionally in a virtual environment
- Create a new PostgreSQL database
- Set the environment variable `DATABASE_URL` to url of the PostgreSQL database in Flask-SQLAlchmeny config format,
  e.g. `postgresql://user:password@localhost:5432/capstone`
- Run `python manage.py db upgrade` to update the database schema
- Set the environment variables for Auth0:
  - `AUTH0_DOMAIN`: `borenx.au.auth0.com`
  - `AUTH0_API_AUDIENCE`: `capstone`
- Set the environment variables for Flask:
  - `FLASK_APP=app.py`
  - `FLASK_DEV=development`
- Run `flask run`
- The app is hosted on http://127.0.0.1:5000/

Tip: Check the file `setup.sh` for setting up environment variables.

### Tests:
To run the tests on your environment:

- All the dependencies in `requirements.txt` needed to be installed.
- Create a new PostgreSQL database for testing purposes (different from the
production/development database). The test will create new tables from scratch and drop them at the end of the test.
- Set up an environment variable `TEST_DATABASE_URL` pointing to the url of
the test database for Flask-SQLAlchemy, e.g. `postgresql://postgres:postgres@localhost:5432/capstone_test`.
- Set up environment variables for Auth0
  - `AUTH0_DOMAIN`: `borenx.au.auth0.com`
  - `AUTH0_API_AUDIENCE`: `capstone`
- Set up environment for the JWTs used in testing authorization:
  - `TEST_CASTING_ASSISTANT_JWT`: Casting assistant JWT, see the *Authorization* section
  - `TEST_CASTING_DIRECTOR_JWT`: Casting director JWT, see the *Authorization* section
  - `TEST_EXECUTIVE_PRODUCER_JWT`: Executive producer JWT, see the *Authorization* section
- Run the command `pytest` in the root directory.

Tip: Check the file `setup.sh` for setting up environment variables.

Tip: If most of the tests fail due to 401 unauthorized, check that the JWTs are valid and haven't expired. 

The tests contain:
- At least one test for success behavior of each endpoint
- At least one test for error behavior of each endpoint
- At least two tests of RBAC for each role