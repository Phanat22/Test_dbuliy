import requests
from jsonschema import validate


GET_MEMBERS_URL = 'http://demo8955896.mockable.io/members'
GET_MEMBER_URL = 'https://demo8955896.mockable.io/member/{member_id}'


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
                       'probation_period': {"type": "string"}
                       },
                  "required": ['position', 'ID', 'day_birth', 'email', 'first_name', 'hr_department', 'last_name',
                               'level', 'mobile', 'probation_period']
                  }
         },
    "required": ["status", "data"]
}


def check_header(res):
    if res.headers.get('Content-Type'):
        assert res.headers['Content-Type'] == 'application/json; charset=UTF-8', "Wrong content type value"
    else:
        assert False, "Content-Type is missing"


class TestAPIGetMembers:

    def test_get_list_members(self):
        res = requests.get(url=GET_MEMBERS_URL)
        assert res.status_code == 200, "Wrong status code"
        check_header(res)
        validate(instance=res.json(), schema=SCHEMA)
        assert len(res.json()["data"]["members"]) == 3, "Wrong count of members"

    def test_get_member(self):
        res = requests.get(url=GET_MEMBERS_URL)
        member_id = res.json()["data"]["members"][0]["ID"]
        res_member = requests.get(url=GET_MEMBER_URL.format(member_id=member_id), verify=False)
        assert res_member.status_code == 200, "Wrong code"
        check_header(res_member)
        validate(instance=res_member.json(), schema=MEMBER_SCHEMA)
        act_member_id = res_member.json()["data"]["ID"]
        assert act_member_id == member_id, f"Wrong member's id, exp={member_id}, act={act_member_id}"
