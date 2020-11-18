from datetime import datetime
import os
import requests
import uuid

def obtain_token_headers():
    # Obtain token
    host = os.environ.get('GOOGLE_CLOUD_HOST_URL')
    response = requests.post(f'https://{host}/api/token/', {
        'email': os.environ.get('CLOUD_FUNCTION_EMAIL'),
        'password': os.environ.get('CLOUD_FUNCTION_PASSWORD'),
    })
    token = response.json()['access']
    headers = {'Authorization': f'Bearer {token}'}
    return headers

def post_hash(project, file, headers, data):
    host = os.environ.get('GOOGLE_CLOUD_HOST_URL')
    # Retrieve photo in order to get its ID
    photo = requests.get(
        url=f'https://{host}/api/photos/?project={project}&search={file}',
        headers=headers,
    ).json()
    if len(photo) == 0:
        print(f'Failed retrieving {file}')
        return
    photo = photo[0]
    hash_id = photo['hash_id']
    # Post data
    response = requests.patch(
        url=f'https://{host}/api/hash/{hash_id}/?project={project}',
        headers=headers,
        data=data
    )
    # Check if hash already exists
    duplicates = requests.get(
        url=f'https://{host}/api/hash/?project={project}&search={data["hash"]}',
        headers=headers,
    ).json()
    if len(duplicates) == 2:
        duplicate_id = str(uuid.uuid4())
        for dup in duplicates:
            requests.patch(
                url=f'https://{host}/api/hash/{dup["id"]}/?project={project}',
                headers=headers,
                data={'duplicate_id': duplicate_id, 'is_duplicated': True, 'status': 1, 'date_status': datetime.now().isoformat()}
            )
    elif len(duplicates) > 2:
        duplicate_id = [d['duplicate_id'] for d in duplicates if d['duplicate_id']][0]
        requests.patch(
            url=f'https://{host}/api/hash/{hash_id}/?project={project}',
            headers=headers,
            data={'duplicate_id': duplicate_id, 'is_duplicated': True, 'status': 1, 'date_status': datetime.now().isoformat()}
        )
    # Success!
    print(f'Post data for {file.name}: response {response}')
    return response
