import os
import requests

def post_photo_data(project, name, payload):
    # Obtain token
    host = os.environ.get('GOOGLE_CLOUD_HOST_URL')
    response = requests.post(f'https://{host}/api/token/', {
        'email': os.environ.get('CLOUD_FUNCTION_EMAIL'),
        'password': os.environ.get('CLOUD_FUNCTION_PASSWORD'),
    })
    token = response.json()['access']
    # Retrieve photo in order to get its ID
    photo = requests.get(
        url=f'https://{host}/api/photos/?project={project}&search={name}',
        headers={'Authorization': f'Bearer {token}'},
    )
    if not photo:
        return
    photo = photo.json()[0]
    photo_id = photo['id']
    # Post data payload
    response = requests.patch(
        url=f'https://{host}/api/photos/{photo_id}/?project={project}',
        data=payload,
        headers={'Authorization': f'Bearer {token}'},
    )
    print(f'Post data for {name}: response {response}')
    return response
