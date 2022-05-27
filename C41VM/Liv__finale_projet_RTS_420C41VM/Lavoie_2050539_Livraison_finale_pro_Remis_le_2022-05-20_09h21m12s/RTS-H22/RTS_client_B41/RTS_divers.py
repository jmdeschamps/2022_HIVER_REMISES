## -*- Encoding: UTF-8 -*-

prochainid = 0


def get_prochain_id() -> str:
    global prochainid
    prochainid += 1
    return f'id_{prochainid}'


