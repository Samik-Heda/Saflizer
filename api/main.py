import os
from flask import Flask, request
from backend import *
from datetime import datetime
from zoneinfo import ZoneInfo
import time
import tzdata

app = Flask('Saflizer')

key = os.environ.get('KEY')

def time_loop():
    data = getdataf()
    for supervisor in data.keys():
        
            for i in range(len(data[supervisor]['time'])):            
                now = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
                supervisortime = datetime.strptime(data[supervisor]['time'][i], '%H:%M')
                if now.minute == supervisortime.minute and now.hour == supervisortime.hour:
                    for driver in data[supervisor]['drivers'].keys():
                        lasttest = data[supervisor]['drivers'][driver]['lasttest']
                        lasttest = lasttest.split(':')
                        lasttest = f'{lasttest[0]}:{lasttest[1]}'
                        if lasttest == "None":
                            alertf(data, supervisor, driver, 'Test not completed')
                            datetimeinfo = datetime.now(tz=ZoneInfo('Asia/Kolkata')).strftime('%d-%m-%Y %H:%M')
                            test = f'{datetimeinfo}: Test not completed'
                            if data[supervisor]['drivers'][driver]['test'] != ['empty']:
                                data[supervisor]['drivers'][driver]['test'].append(test)
                            else:
                                data[supervisor]['drivers'][driver]['test'] = [test]
                            break
                        else:
                            if ((datetime.strptime(lasttest, '%d-%m-%Y %H:%M') - supervisortime).total_seconds() / 60) < 31 and ((datetime.strptime(lasttest, '%d-%m-%Y %H:%M') - supervisortime).total_seconds() / 60) > 0 and data[supervisor]['drivers'][driver]['duty'] == 'True':
                                pass
                            else:
                                alertf(data, supervisor, driver, 'Test not completed')
                                datetimeinfo = datetime.now(tz=ZoneInfo('Asia/Kolkata')).strftime('%d-%m-%Y %H:%M')
                                test = f'{datetimeinfo}: Test not completed'
                                if data[supervisor]['drivers'][driver]['test'] != ['empty']:
                                    data[supervisor]['drivers'][driver]['test'].append(test)
                                else:
                                    data[supervisor]['drivers'][driver]['test'] = [test]
                                break
        
    time.sleep(30)
    time_loop()

@app.route('/')
def home():
    return "IKEA BOYS API is running"

@app.route('/getdata', methods=['POST'])
def getdata():
    data = request.form
    if data['apikey'] == key:
        data = getdataf()
        images = {}
        for i in data.keys():
            try:
                for j in data[i]['drivers'].keys():
                    images[data[i]['drivers'][j]['image']] = j
            except:
                continue
        return images
    else:
        return "401"
    
@app.route('/signup', methods=['POST'])
def signup():
    data = request.form
    if data['apikey'] == key:
        username = request.form['username']
        password = request.form['password']
        data = getdataf()
        if username in data.keys():
            return "403"
        data[username] = {'password':password, 'drivers':'None', 'alerts':['empty'], 'time':['empty']}
        uploaddataf(data)
        return "200"
    else:
        return "401"
    
@app.route('/login', methods=['POST'])
def login():
    data = request.form
    if data['apikey'] == key:
        username = request.form['username']
        password = request.form['password']
        data = getdataf()
        if username not in data.keys():
            return "404"
        if password == data[username]['password']:
            return "200"
        else:
            return "409"
    else:
        return "401"
    
@app.route('/adddriver', methods=['POST'])
def adddriver():
    data = request.form
    if data['apikey'] == key:
        username = request.form['username']
        name = request.form['name']
        image = request.files['image'].read()
        image = base64.b64encode(image).decode('utf-8')
        data = getdataf()
        if username not in data.keys():
            return "403"
        driverid = genid(data[username])
        if data[username]['drivers'] != 'None':
            data[username]['drivers'][driverid] = {'name':name, 'image':image, 'duty':True, 'test':['empty'], "lasttest": "None"}
        else:
            data[username]['drivers'] = {driverid:{'name':name, 'image':image, 'duty':True, 'test':['empty'], "lasttest": "None"}}
        uploaddataf(data)
        return "200"
    else:
        return "401"
    
@app.route('/getdriverinfo', methods=['POST'])
def getdriverinfo():
    data = request.form
    if data['apikey'] == key:
        driverid = request.form['id']
        username = request.form['username']
        data = getdataf()
        if username not in data.keys():
            return "403"
        return data[username]['drivers'][driverid]
    else:
        return "401"
    
@app.route('/getdrivers', methods=['POST'])
def getdrivers():
    data = request.form
    if data['apikey'] == key:
        username = request.form['username']
        data = getdataf()
        if username not in data.keys():
            return "403"
        ids = []
        if data[username]['drivers'] == 'None':
            return {'ids':ids}
        for i in data[username]['drivers'].keys():
            ids.append(i)
        return {'ids':ids}
    else:
        return "401"
    
@app.route('/deletedriver', methods=['POST'])
def deletedriver():
    data = request.form
    if data['apikey'] == key:
        username = request.form['username']
        driverid = request.form['id']
        data = getdataf()
        if username not in data.keys():
            return "403"
        data[username]['drivers'].pop(driverid)
        if data[username]['drivers'] == {}:
            data[username]['drivers'] = 'None'
        uploaddataf(data)
        return "200"
    else:
        return "401"
    
@app.route('/editdriver', methods=['POST'])
def editdriver():
    data = request.form
    if data['apikey'] == key:
        username = request.form['username']
        driverid = request.form['id']
        image = request.files['image']
        name = request.form['name']
        data = getdataf()
        if username not in data.keys():
            return "403"
        if image != "None":
            image = image.read()
            image = base64.b64encode(image).decode('utf-8')
            data[username]['drivers'][driverid]['image'] = image
        if name != "None":
            data[username]['drivers'][driverid]['name'] = name
        uploaddataf(data)
        return "200"
    else:
        return "401"
    
@app.route('/duty', methods=['POST'])
def duty():
    data = request.form
    if data['apikey'] == key:
        username = request.form['username']
        driverid = request.form['id']
        duty = request.form['duty']
        data = getdataf()
        if username not in data.keys():
            return "403"
        data[username]['drivers'][driverid]['duty'] = duty
        uploaddataf(data)
        return "200"
    else:
        return "401"
    
@app.route('/logtest', methods=['POST'])
def logtest():
    data = request.form
    if data['apikey'] == key:
        username = request.form['username']
        driverid = request.form['id']
        test = request.form['test']
        data = getdataf()
        if username not in data.keys():
            return "403"
        if int(test.replace(' mg/l', '')) > 30 and str(data[username]['drivers'][driverid]['duty']) == 'True':
            alertf(data, username, driverid, test)
            datetimeinfo = datetime.now(tz=ZoneInfo('Asia/Kolkata')).strftime('%d-%m-%Y %H:%M')
            test = f'{datetimeinfo}: {test}'
            if data[username]['drivers'][driverid]['test'] != ['empty']:
                data[username]['drivers'][driverid]['test'].append(test)
            else:
                data[username]['drivers'][driverid]['test'] = [test]
        data[username]['drivers'][driverid]['lasttest'] = str(datetimeinfo)
        uploaddataf(data)
        return "200"
    else:
        return "401"
    
@app.route('/alerts', methods=['POST'])
def alerts():
    data = request.form
    if data['apikey'] == key:
        username = request.form['username']
        data = getdataf()
        if username not in data.keys():
            return "403"
        alerts_var = data[username]['alerts']
        if alerts_var == ['empty']:
            return {'alerts':[]}
        data[username]['alerts'] = ['empty']
        uploaddataf(data)
        return {'alerts':alerts_var}
    else:
        return "401"

@app.route('/tests', methods=['POST'])
def tests():
    data = request.form
    if data['apikey'] == key:
        username = request.form['username']
        driverid = request.form['id']
        data = getdataf()
        if username not in data.keys():
            return "403"
        tests = data[username]['drivers'][driverid]['test']
        if tests == ['empty']:
            return {'tests':[]}
        return {'tests':tests}
    else:
        return "401"
    
@app.route('/addtime', methods=['POST'])
def addtime():
    data = request.form
    if data['apikey'] == key:
        username = request.form['username']
        time = request.form['time']
        data = getdataf()
        if username not in data.keys():
            return "403"
        if data[username]['time'] != ['empty']:
            data[username]['time'].append(time)
        else:
            data[username]['time'] = [time]
        uploaddataf(data)
        return "200"
    else:
        return "401"
    
@app.route('/removetime', methods=['POST'])
def removetime():
    data = request.form
    if data['apikey'] == key:
        username = request.form['username']
        time = request.form['time']
        data = getdataf()
        if username not in data.keys():
            return "403"
        data[username]['time'].pop(data[username]['time'].index(time))
        if data[username]['time'] == []:
            data[username]['time'] = ['empty']
        uploaddataf(data)
        return "200"
    else:
        return "401"
    
@app.route('/gettimes', methods=['POST'])
def gettimes():
    data = request.form
    if data['apikey'] == key:
        username = request.form['username']
        data = getdataf()
        if username not in data.keys():
            return "403"
        times = data[username]['time']
        if times == ['empty']:
            times = []
        return {'times':times}
    else:
        return "401"

Thread(target=time_loop).start()
app.run(host='0.0.0.0',port=8080)
