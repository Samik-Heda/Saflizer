import base64
import firebase_admin
from firebase_admin import credentials, db
from threading import Thread


def _init_database():
    cred = credentials.Certificate("firebase_cred.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://saflizer-default-rtdb.firebaseio.com/'})
    global ref
    ref = db.reference("/")


def uploaddataf(data):
    Thread(target=ref.set, args=(data,)).start()


def getdataf():
    data = ref.get()
    return data


def genid(data):
    data = data['drivers']
    if data == 'None':
        return 'driver0'
    ids = []
    for i in data.keys():
        ids.append(int(i.replace('driver', '')))
    return f'driver{max(ids) + 1}'


def alertf(data, username, driverid, test):
    if data[username]['alerts'] != ['empty']:
        data[username]['alerts'].append(f'{driverid}:{test}')
    else:
        data[username]['alerts'] = [f'{driverid}:{test}']
    uploaddataf(data)


def encode_dataf(text: str):
    text = text.encode('ascii')
    text = base64.b64encode(text)
    return text


def decode_dataf(text: str):
    text = base64.b64decode(text)
    text = text.decode('utf-8')
    return str(text)


_init_database()