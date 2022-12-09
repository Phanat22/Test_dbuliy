import pytest
import requests
from jsonschema import validate

SCHEMA = {
    "type": "object",
    "properties":
        {'status': {"type": "string"},
         'data': {"type": "object",
                  "properties":
                      {'members': {"type": "array",
                                   "items": {"type": "object",
                                             "properties":
                                                 {'ID': {"type": "string"},
                                                  'day_birth': {"type": "number"},
                                                  'email': {"type": "string"},
                                                  'first_name': {"type": "string"},
                                                  'hr_department': {"type": "string"},
                                                  'last_name': {"type": "string"},
                                                  'level': {"type": "string"},
                                                  'mobile': {"type": "integer"},
                                                  'position': {"type": "string"},
                                                  'probation_period': {"type": "integer"},
                                                  },
                                             "required": ['ID', 'day_birth', 'email', 'first_name',
                                                          'hr_department', 'last_name', 'level', 'mobile', 'position',
                                                          'probation_period'],
                                             },

                                   }
                       }, "required": ['members']

                  },

         },
    "required": ['status', 'data'],
}

MEMBER_SCHEMA = {
    "type": "object",
    "properties":
        {'status': {"type": "string"},
         'data': {"type": "object",
                  "properties":
                      {'position': {"type": "string"},
                         'ID': {"type": "string"},
                          'day_birth': {"type": "number"},
                          'email': {"type": "string"},
                          'first_name': {"type": "string"},
                          'hr_department': {"type": "string"},
                          'last_name': {"type": "string"},
                          'level': {"type": "string"},
                          'mobile': {"type": "integer"},
                          'probation_period': {"type": "string"},
                        },
                  "required": ['position', 'ID', 'day_birth', 'email', 'first_name', 'hr_department', 'last_name',
                               'level', 'mobile', 'probation_period']
                  }
         },
    "required": ["status", "data"]
}


def check_header(res):
    new_dict = {}
    for k, v in res.headers.items():
        if k == 'Content-Type':
            new_dict.update({k: v})

    assert {'Content-Type': 'application/json; charset=UTF-8'} == new_dict, "Wrong header"

def test_one():
    res = requests.get(url='http://demo8955896.mockable.io/members')
    assert res.status_code == 200, "Wrong status code"
    check_header(res)
    validate(instance=res.json(), schema=SCHEMA)

def test_two():
    res = requests.get(url='http://demo8955896.mockable.io/members')
    member_id = res.json()["data"]["members"][0]["ID"]
    res = requests.get(url=f'https://demo8955896.mockable.io/member/{member_id}', verify=False)
    assert res.status_code == 200, "Wrong code"
    check_header(res)
    validate(instance=res.json(), schema=MEMBER_SCHEMA)
