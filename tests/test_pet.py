import os

import pytest
import requests
from jsonschema import validate

from pages.class_assertion import Assertion

PET_URL = 'https://petstore.swagger.io/v2/pet'
PET_FIND_BY_STATUS_URL = 'https://petstore.swagger.io/v2/pet/findByStatus'
PATH_TO_LOCAL_FOLDER = os.path.join(os.path.dirname(__file__), "upload_files")

PET_DATA = {
  "id": 0,
  "category": {
    "id": 0,
    "name": "string"
  },
  "name": "doggie",
  "photoUrls": [
    "string"
  ],
  "tags": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "status": "available"
}

PET_DATA_PENDING = PET_DATA.copy()
PET_DATA_PENDING.update({"status": "pending"})

PET_DATA_SOLD = PET_DATA.copy()
PET_DATA_SOLD.update({"status": "sold"})


CREATE_PET_SCHEMA = {
    "type": "object",
    "properties":
        {'id': {"type": "integer"},
         'category': {"type": "object",
                      "properties":
                          {'id': {"type": "integer"},
                           'name': {"type": "string"},
                           },
                      "required": ['id', 'name']},
         'name': {"type": "string"},
         'photoUrls': {
             "type": "array",
             "items": {'type': 'string'},
         },
         'tags': {
             "type": "array",
             "items": {
                 "type": "object",
                 "properties": {
                     "id": {'type': 'integer'},
                     "name": {'type': "string"}
                 },
                 "required": ['id', 'name']
             }
         },
         'status': {'type': "string"},
         },
    "required": ["id", "category", "status", "tags", "photoUrls"]
}


def check_header(res):
    if res.headers.get('Content-Type'):
        assert res.headers['Content-Type'] == 'application/json', "Wrong content type value"
    else:
        assert False, "Content-Type is missing"


class TestPet:

    def test_create_pet(self):
        res = requests.post(url=PET_URL, json=PET_DATA, verify=False)
        assert res.status_code == 200, "Wrong status code"
        check_header(res)
        validate(instance=res.json(), schema=CREATE_PET_SCHEMA)
        _assert = Assertion()
        _assert.add(res.json().get('id') != PET_DATA['id'], "Wrong ID, ID is not changed")\
            .add(res.json().get('status') == PET_DATA['status'], "wrong status")\
            .do_assert()

    @pytest.mark.parametrize('data', [0, -1, '1', 1.1, ' '])
    def test_create_pet_by_id(self, data):
        res = requests.post(url=PET_URL, json={'id': data}, verify=False)
        assert res.status_code == 200, "Wrong status code"
        check_header(res)

        _assert = Assertion()
        _assert.add(res.json().get('id') != data, "Wrong ID, ID is not changed")\
            .add(len(res.json().get('photoUrls')) == 0, "Wrong data of photoUrls")\
            .add(len(res.json().get('tags')) == 0, "Wrong data of tags")\
            .add(len(res.json()) == 3, "wrong count of items")\
            .do_assert()

    @pytest.mark.parametrize('data', ['A', 'a', '!@#$'])
    def test_neg_create_pet_by_id(self, data):
        res = requests.post(url=PET_URL, json={'id': data}, verify=False)
        assert res.status_code == 500, "Wrong status code"  # maybe we should get another status code and it is a bug

    @pytest.mark.parametrize('data', [1, '1', ' ', '!@#$', 0.1, None])
    def test_neg_create_pet(self, data):
        res = requests.post(url=PET_URL, json=data, verify=False)
        if data is None:
            assert res.status_code == 415, "Wrong status code"
        else:
            assert res.status_code == 500, "Wrong status code" # maybe we should get another status code and it is a bug

    @pytest.mark.parametrize('file', ['image.png', 'Test.txt'])
    def test_pet_upload_image(self, file):
        create_pet_res = requests.post(url=PET_URL, json=PET_DATA, verify=False)
        pet_id = create_pet_res.json()['id']
        files = [
            ('file', (file, open(f'{PATH_TO_LOCAL_FOLDER}/{file}', 'rb'), 'image/jpeg'))
        ]
        res = requests.post(url=f'{PET_URL}/{pet_id}/uploadImage', files=files, verify=False)
        check_header(res)

        _assert = Assertion()
        _assert.add(res.json().get('code') == 200, "Wrong status code")\
            .add(file in res.json().get('message'), "Wrong message data")\
            .do_assert()

    @pytest.mark.parametrize('data, status', [(' ', 404), ('!@#$', 415), (0.1, 404), (None, 404)])
    def test_neg_pet_upload_image_wrong_id(self, data, status):
        files = [
            ('file', ('image.png', open(f'{PATH_TO_LOCAL_FOLDER}/image.png', 'rb'), 'image/jpeg'))
        ]
        res = requests.post(url=f'{PET_URL}/{data}/uploadImage', files=files, verify=False)
        assert res.status_code == status, "Wrong status code"

    def test_neg_pet_upload_image(self):
        create_pet_res = requests.post(url=PET_URL, json=PET_DATA, verify=False)
        pet_id = create_pet_res.json()['id']
        res = requests.post(url=f'{PET_URL}/{pet_id}/uploadImage', verify=False)
        assert res.status_code == 415, "Wrong status code"

    def test_put_pet(self):
        res = requests.put(url=PET_URL, json=PET_DATA, verify=False)
        assert res.status_code == 200, "Wrong status code"
        check_header(res)
        validate(instance=res.json(), schema=CREATE_PET_SCHEMA)
        _assert = Assertion()
        _assert.add(res.json().get('id') != PET_DATA['id'], "Wrong ID, ID is not changed")\
            .add(res.json().get('status') == PET_DATA['status'], "wrong status")\
            .do_assert()

    @pytest.mark.parametrize('status, schema', [
        ('available', PET_DATA),
        ('pending', PET_DATA_PENDING),
        ('sold', PET_DATA_SOLD),
    ])
    def test_get_pet(self, status, schema):
        requests.put(url=PET_URL, json=schema, verify=False)
        res = requests.get(url=PET_FIND_BY_STATUS_URL, params={'status': status}, verify=False)
        assert res.status_code == 200, "Wrong status code"
        check_header(res)

        _assert = Assertion()
        _assert\
            .add(len(res.json()) != 0, "Error, list is empty")\
            .add(res.json()[0]['status'] == status, "Wrong status")\
            .do_assert()

    def test_find_pet_by_id(self):
        res = requests.put(url=PET_URL, json=PET_DATA, verify=False)
        pet_id = res.json()['id']
        get_res = requests.get(url=f'{PET_URL}/{pet_id}', verify=False)
        check_header(res)
        assert res.status_code == 200, "Wrong status code"
        assert get_res.json()['id'] == pet_id, "Wrong pet id"
        validate(instance=get_res.json(), schema=CREATE_PET_SCHEMA)

    @pytest.mark.parametrize('data, status_code', [('', 405), ('1.0', 404), ('!@#$%^&', 404), (None, 404)])
    def test_neg_find_pet_by_id(self, data, status_code):
        get_res = requests.get(url=f'{PET_URL}/{data}', verify=False)
        assert get_res.status_code == status_code, "Wrong status code"

    def test_delete_pet(self):
        res = requests.put(url=PET_URL, json=PET_DATA, verify=False)
        pet_id = res.json()['id']
        delete_res = requests.delete(url=f'{PET_URL}/{pet_id}', json=PET_DATA, verify=False)
        assert delete_res.status_code == 200, "Wrong status code"
        check_header(res)
        assert delete_res.json()['message'] == str(pet_id), "Wrong id was deleted"
        get_res = requests.get(url=f'{PET_URL}/{pet_id}', verify=False)
        assert get_res.status_code == 404, "Wrong status code"

    @pytest.mark.parametrize('data, status_code', [('', 405), ('1.0', 404), ('!@#$%^&', 404), (None, 404)])
    def test_neg_delete_pet(self, data, status_code):
        delete_res = requests.delete(url=f'{PET_URL}/{data}', json=PET_DATA, verify=False)
        assert delete_res.status_code == status_code, "Wrong status code"

    def test_update_pet_with_form_data(self):
        res = requests.post(url=PET_URL, json=PET_DATA, verify=False)
        pet_id = res.json()['id']
        update_res = requests.post(url=f'{PET_URL}/{pet_id}', data={"name": "test"}, verify=False)
        check_header(update_res)
        assert update_res.status_code == 200, "Wrong status code"
        assert update_res.json()['message'] == str(pet_id), "Wrong ID"

    @pytest.mark.parametrize('data, status_code', [('', 415), ('1.0', 404), ('!@#$%^&', 404), (None, 404)])
    def test_neg_update_pet_with_form_data(self, data, status_code):
        update_res = requests.post(url=f'{PET_URL}/{data}', data={"name": "test"}, verify=False)
        assert update_res.status_code == status_code, "Wrong status code"
