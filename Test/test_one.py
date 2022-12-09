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

def test_one():
    res = requests.get(url='http://demo8955896.mockable.io/members')
    assert res.status_code == 200, "Wrong status code"
    validate(instance=res.json(), schema=SCHEMA)
