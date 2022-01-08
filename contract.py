import datetime as dt

from requests import HTTPError

import eospy.cleos
import eospy.keys
import yaml

import logger
from eospy.types import Abi, Action
from eospy.utils import parse_key_file
import os
import pytz
import json
from settings import load_user_param, user_param
from logger import log

def push_transaction(params_json):
    # this url is to a testnet that may or may not be working.
    # We suggest using a different testnet such as kylin or jungle
    #
    ce = eospy.cleos.Cleos(url=user_param.rpc_domain)

    # arguments = {
    #     "from": "openfarmercn",  # sender
    #     "to": "4lrzu.wam",
    #     "quantities": ["0.0001 FWF"],
    #     "memo": "openfarmercn",
    # }
    # payload = {
    #     "account": "farmerstoken",
    #     "name": "transfers",
    #     "authorization": [{
    #         "actor": "openfarmercn",
    #         "permission": "active",
    #     }],
    # }
    arguments = params_json['actions'][0]['data']
    payload = {
        "account": params_json['actions'][0]['account'],
        "name": params_json['actions'][0]['name'],
        "authorization": params_json['actions'][0]['authorization'],
    }

    # Converting payload to binary
    data = ce.abi_json_to_bin(payload['account'], payload['name'], arguments)
    # Inserting payload binary form as "data" field in original payload
    payload['data'] = data['binargs']
    # final transaction formed
    trx = {"actions": [payload]}
    trx['expiration'] = str(
        (dt.datetime.utcnow() + dt.timedelta(seconds=60)).replace(tzinfo=pytz.UTC))
    # use a string or EOSKey for push_transaction
    # key = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
    # use EOSKey:
    log.info(user_param.private_key)
    key = eospy.keys.EOSKey(user_param.private_key)
    try:
        resp = ce.push_transaction(trx, key, broadcast=True)
        return True, resp
    except HTTPError as e:
        log.info(str(e))
        return False, str(e)





def testTransfers():
    transaction = {
        "actions": [{
            "account": "farmerstoken",
            "name": "transfers",
            "authorization": [{
                "actor": "openfarmercn",
                "permission": "active",
            }],
            "data": {
                "from": "openfarmercn",
                "to": "4lrzu.wam",
                "quantities": ["0.0001 FWF"],
                "memo": "openfarmercn",
            },
        }],
    }
    push_transaction(transaction)


def testClaim():
    transaction = {
        "actions": [{
            "account": "farmersworld",
            "name": "claim",
            "authorization": [{
                "actor": "openfarmercn",
                "permission": "active",
            }],
            "data": {
                "asset_id": "1099586565781",
                "owner": "openfarmercn",
            },
        }],
    }
    push_transaction(transaction)


if __name__ == '__main__':
    with open('user.yml', "r", encoding="utf8") as file:
        user: dict = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
    load_user_param(user)
    logger.init_loger(user_param.wax_account)
    testClaim()
