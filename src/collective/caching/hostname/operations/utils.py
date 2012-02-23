# -*- coding:utf-8 -*-


def getHostname(request):
    ''' Get the hostname of the request '''
    hostname = ''
    # Using VHM
    if 'VIRTUAL_URL_PARTS' in request:
        parts = request.get('VIRTUAL_URL_PARTS', [])
        hostname = parts and parts[0] or ''

    if not hostname:
        hostname = request.get('SERVER_URL', '')
    return hostname
