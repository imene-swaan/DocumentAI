
from typing import Dict
from pydantic import BaseModel, validator
import re

class Entity(BaseModel):
    address: str
    taxID: str
    num: str
    email:str
    fax: str

    @validator('email')
    def valid_email(cls, v):
        pattern = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not re.search(pattern, v):
            return ''
        return v
    @validator('fax', 'num')
    def valid_num(cls, v):
        if len(v) != 12:
            return ''
        for i in range(12):
            if i in [3, 7]:
                if v[i] != '-':
                    return ''
            elif not v[i].isalnum():
                return ''
        return v
def process_result(result: Dict):
    if result['prob'] < 0.7:
        return ''
    return result['value']
