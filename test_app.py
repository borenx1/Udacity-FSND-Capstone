import os
import pytest
from app import create_app
from models import Actor, Movie


@pytest.fixture
def client():
    app = create_app(test_config=True)
    # Build up test database from scratch
    app.db.drop_all()
    app.db.create_all()
    client = app.test_client()

    yield client

    # Drop all tables from the database after testing
    app.db.drop_all()


@pytest.fixture
def casting_assistant_jwt():
    jwt = os.environ['TEST_CASTING_ASSISTANT_JWT']
    return jwt


@pytest.fixture
def casting_director_jwt():
    jwt = os.environ['TEST_CASTING_DIRECTOR_JWT']
    return jwt


@pytest.fixture
def executive_producer_jwt():
    jwt = os.environ['TEST_EXECUTIVE_PRODUCER_JWT']
    return jwt


def test_get_actors(client, casting_assistant_jwt):
    response = client.get('/actors',
                          headers={'authorization': f'Bearer {casting_assistant_jwt}'})
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_actors_fail_auth(client):
    # Get actors with authorization
    response = client.get('/actors')
    assert response.status_code == 401


def test_get_movies(client, casting_assistant_jwt):
    response = client.get('/movies',
                          headers={'authorization': f'Bearer {casting_assistant_jwt}'})
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_movies_fail_auth(client):
    # Get movies with authorization
    response = client.get('/movies')
    assert response.status_code == 401


def test_post_actor(client, casting_director_jwt):
    body = {'name': 'John', 'age': 40, 'gender': 'M'}
    response = client.post('/actors',
                           json=body,
                           headers={'authorization': f'Bearer {casting_director_jwt}'})
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['id']


def test_post_actor_fail(client, casting_director_jwt):
    # Missing body
    response = client.post('/actors',
                           headers={'authorization': f'Bearer {casting_director_jwt}'})
    assert response.status_code == 400

    # Missing age
    body = {'name': 'John'}
    response = client.post('/actors',
                           json=body,
                           headers={'authorization': f'Bearer {casting_director_jwt}'})
    assert response.status_code == 400


def test_post_actor_fail_negative_age(client, casting_director_jwt):
    # Fail due to negative age
    body = {'name': 'John', 'age': -11, 'gender': 'M'}
    response = client.post('/actors',
                           json=body,
                           headers={'authorization': f'Bearer {casting_director_jwt}'})
    assert response.status_code == 422


def test_post_actor_fail_auth(client):
    body = {'name': 'John', 'age': 40, 'gender': 'M'}
    response = client.post('/actors', json=body)
    assert response.status_code == 401


def test_post_actor_fail_permission(client, casting_assistant_jwt):
    body = {'name': 'John', 'age': 40, 'gender': 'M'}
    response = client.post('/actors',
                           json=body,
                           headers={'authorization': f'Bearer {casting_assistant_jwt}'})
    assert response.status_code == 403


def test_post_movie(client, executive_producer_jwt):
    body = {'title': 'Movie A', 'release_date': '2021-01-01'}
    response = client.post('/movies',
                           json=body,
                           headers={'authorization': f'Bearer {executive_producer_jwt}'})
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['id']


def test_post_movie_fail(client, executive_producer_jwt):
    # Missing body
    response = client.post('/movies',
                           headers={'authorization': f'Bearer {executive_producer_jwt}'})
    assert response.status_code == 400

    # Missing release_date
    body = {'title': 'Movie B'}
    response = client.post('/movies',
                           json=body,
                           headers={'authorization': f'Bearer {executive_producer_jwt}'})
    assert response.status_code == 400


def test_post_movie_fail_date_format(client, executive_producer_jwt):
    # Fail due to incorrect date format
    body = {'title': 'Movie C', 'release_date': '01-02-2020'}
    response = client.post('/movies',
                           json=body,
                           headers={'authorization': f'Bearer {executive_producer_jwt}'})
    assert response.status_code == 422
    # No 0 padding in day (not ISO 8601 format)
    body = {'title': 'Movie D', 'release_date': '2019-11-1'}
    response = client.post('/movies',
                           json=body,
                           headers={'authorization': f'Bearer {executive_producer_jwt}'})
    assert response.status_code == 422


def test_post_movie_fail_auth(client):
    body = {'title': 'Movie A', 'release_date': '2021-01-01'}
    response = client.post('/movies', json=body)
    assert response.status_code == 401


def test_post_movie_fail_permission(client, casting_director_jwt):
    body = {'title': 'Movie A', 'release_date': '2021-01-01'}
    response = client.post('/movies',
                           json=body,
                           headers={'authorization': f'Bearer {casting_director_jwt}'})
    assert response.status_code == 403


def test_patch_actor_age(client, casting_director_jwt):
    # Insert a new actor to update
    response = client.post('/actors',
                           json={'name': 'Test', 'age': 44, 'gender': 'F'},
                           headers={'authorization': f'Bearer {casting_director_jwt}'})
    actor_id = response.get_json()['id']
    new_age = 99
    response = client.patch(f'/actors/{actor_id}',
                            json={'age': new_age},
                            headers={'authorization': f'Bearer {casting_director_jwt}'})
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['id'] == actor_id
    assert response_data['age'] == new_age
    actor = Actor.query.get(actor_id)
    # Close the session to prevent holding up the test after accessing the database
    client.application.db.session.close()
    assert actor.age == new_age


def test_patch_actor_name(client, casting_director_jwt, executive_producer_jwt):
    # Insert a new actor to update
    response = client.post('/actors',
                           json={'name': 'Test', 'age': 44, 'gender': 'F'},
                           headers={'authorization': f'Bearer {casting_director_jwt}'})
    actor_id = response.get_json()['id']
    new_name = 'New Name'
    response = client.patch(f'/actors/{actor_id}',
                            json={'name': new_name},
                            headers={'authorization': f'Bearer {executive_producer_jwt}'})
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['id'] == actor_id
    assert response_data['name'] == new_name
    actor = Actor.query.get(actor_id)
    # Close the session to prevent holding up the test after accessing the database
    client.application.db.session.close()
    assert actor.name == new_name


def test_patch_actor_fail(client, casting_director_jwt):
    # Insert a new actor to update
    response = client.post('/actors',
                           json={'name': 'Test', 'age': 44, 'gender': 'F'},
                           headers={'authorization': f'Bearer {casting_director_jwt}'})
    actor_id = response.get_json()['id']

    # No body in request
    response = client.patch(f'/actors/{actor_id}',
                            headers={'authorization': f'Bearer {casting_director_jwt}'})
    assert response.status_code == 400

    # Negative age
    response = client.patch(f'/actors/{actor_id}',
                            json={'age': -1},
                            headers={'authorization': f'Bearer {casting_director_jwt}'})
    assert response.status_code == 422


def test_patch_actor_fail_does_not_exist(client, casting_director_jwt):
    response = client.patch('/actors/99999',
                            headers={'authorization': f'Bearer {casting_director_jwt}'})
    assert response.status_code == 404


def test_patch_actor_fail_auth(client):
    actor_id = 1
    response = client.patch(f'/actors/{actor_id}')
    assert response.status_code == 401


def test_patch_actor_fail_permission(client, casting_assistant_jwt):
    actor_id = 1
    response = client.patch(f'/actors/{actor_id}',
                            headers={'authorization': f'Bearer {casting_assistant_jwt}'})
    assert response.status_code == 403


def test_patch_movie_title(client, casting_director_jwt, executive_producer_jwt):
    # Insert a new movie to update
    response = client.post('/movies',
                           json={'title': 'Test', 'release_date': '2020-01-01'},
                           headers={'authorization': f'Bearer {executive_producer_jwt}'})
    movie_id = response.get_json()['id']
    new_title = 'New Title'
    response = client.patch(f'/movies/{movie_id}',
                            json={'title': new_title},
                            headers={'authorization': f'Bearer {casting_director_jwt}'})
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['id'] == movie_id
    assert response_data['title'] == new_title
    movie = Movie.query.get(movie_id)
    # Close the session to prevent holding up the test after accessing the database
    client.application.db.session.close()
    assert movie.title == new_title


def test_patch_movie_release_date(client, casting_director_jwt, executive_producer_jwt):
    # Insert a new movie to update
    response = client.post('/movies',
                           json={'title': 'Test', 'release_date': '2020-01-01'},
                           headers={'authorization': f'Bearer {executive_producer_jwt}'})
    movie_id = response.get_json()['id']
    new_release_date = '2000-12-31'
    response = client.patch(f'/movies/{movie_id}',
                            json={'release_date': new_release_date},
                            headers={'authorization': f'Bearer {casting_director_jwt}'})
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['id'] == movie_id
    assert response_data['release_date'] == new_release_date
    movie = Movie.query.get(movie_id)
    # Close the session to prevent holding up the test after accessing the database
    client.application.db.session.close()
    assert movie.release_date.isoformat() == new_release_date


def test_patch_movie_fail(client, casting_director_jwt, executive_producer_jwt):
    # Insert a new movie to update
    response = client.post('/movies',
                           json={'title': 'Test', 'release_date': '2020-01-01'},
                           headers={'authorization': f'Bearer {executive_producer_jwt}'})
    movie_id = response.get_json()['id']

    # No body in request
    response = client.patch(f'/movies/{movie_id}',
                            headers={'authorization': f'Bearer {casting_director_jwt}'})
    assert response.status_code == 400

    # Invalid date format
    response = client.patch(f'/movies/{movie_id}',
                            json={'release_date': '01-01-2020'},
                            headers={'authorization': f'Bearer {casting_director_jwt}'})
    assert response.status_code == 422


def test_patch_movie_fail_does_not_exist(client, casting_director_jwt):
    response = client.patch('/movies/99999',
                            headers={'authorization': f'Bearer {casting_director_jwt}'})
    assert response.status_code == 404


def test_patch_movie_fail_auth(client):
    movie_id = 1
    response = client.patch(f'/movies/{movie_id}')
    assert response.status_code == 401


def test_patch_movie_fail_permission(client, casting_assistant_jwt):
    movie_id = 1
    response = client.patch(f'/movies/{movie_id}',
                            headers={'authorization': f'Bearer {casting_assistant_jwt}'})
    assert response.status_code == 403


def test_delete_actor(client, casting_director_jwt, executive_producer_jwt):
    # Insert a new actor to update
    response = client.post('/actors', json={'name': 'Test', 'age': 44, 'gender': 'F'},
                           headers={'authorization': f'Bearer {casting_director_jwt}'})
    actor_id = response.get_json()['id']

    response = client.delete(f'/actors/{actor_id}',
                             headers={'authorization': f'Bearer {executive_producer_jwt}'})
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['id'] == actor_id
    # Check if the actor is deleted from the database
    actor = Actor.query.get(actor_id)
    # Close the session to prevent holding up the test after accessing the database
    client.application.db.session.close()
    assert actor is None


def test_delete_actor_fail_does_not_exist(client, executive_producer_jwt):
    response = client.delete('/actors/99999',
                             headers={'authorization': f'Bearer {executive_producer_jwt}'})
    assert response.status_code == 404


def test_delete_actor_fail_auth(client):
    actor_id = 1
    response = client.delete(f'/actors/{actor_id}')
    assert response.status_code == 401


def test_delete_actor_fail_permission(client, casting_assistant_jwt):
    actor_id = 1
    response = client.delete(f'/actors/{actor_id}',
                             headers={'authorization': f'Bearer {casting_assistant_jwt}'})
    assert response.status_code == 403


def test_delete_movie(client, executive_producer_jwt):
    # Insert a new movie to update
    response = client.post('/movies',
                           json={'title': 'Test', 'release_date': '2020-01-01'},
                           headers={'authorization': f'Bearer {executive_producer_jwt}'})
    movie_id = response.get_json()['id']

    response = client.delete(f'/movies/{movie_id}',
                             headers={'authorization': f'Bearer {executive_producer_jwt}'})
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['id'] == movie_id
    # Check if the movie is deleted from the database
    movie = Movie.query.get(movie_id)
    # Close the session to prevent holding up the test after accessing the database
    client.application.db.session.close()
    assert movie is None


def test_delete_movie_fail_does_not_exist(client, executive_producer_jwt):
    response = client.delete('/movies/99999',
                             headers={'authorization': f'Bearer {executive_producer_jwt}'})
    assert response.status_code == 404


def test_delete_movie_fail_auth(client):
    movie_id = 1
    response = client.delete(f'/movies/{movie_id}')
    assert response.status_code == 401


def test_delete_movie_fail_permission(client, casting_assistant_jwt):
    movie_id = 1
    response = client.delete(f'/movies/{movie_id}',
                             headers={'authorization': f'Bearer {casting_assistant_jwt}'})
    assert response.status_code == 403


def test_404_error(client):
    response = client.get('/doesnotexist')
    assert response.status_code == 404
    response_data = response.get_json()
    assert response_data['error'] == 404
    assert response_data['message'] == 'not found'
