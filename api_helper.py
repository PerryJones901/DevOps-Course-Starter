import env_vars as env
import os
import requests

def params_with_auth(params) -> dict:
    return {"key": env.KEY, "token": env.TOKEN, **params}

def get(url, params={}) -> dict:
    return requests.get(url, params=params_with_auth(params)).json()

def post(url, params={}) -> dict:
    return requests.post(url, params=params_with_auth(params)).json()

def put(url, params={}) -> dict:
    return requests.put(url, params=params_with_auth(params)).json()

def delete(url, params={}) -> dict:
    return requests.delete(url, params=params_with_auth(params)).json()
