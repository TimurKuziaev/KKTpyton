# -*- coding: utf-8 -*-

import datetime
import requests  # модуль для работы с post-запросами. установка: pip install requests
import json
import pprint
import easygui   # модуль для работы с окнами. установка: pip install easygui
dt_start = datetime.datetime.now()
dt_string = dt_start.strftime('%y/%m/%d %H:%M:%S')

sText=''
sText2='';
s70='----------------------------------------------------------------------\n'
s99='****************************************************************************************************\n'
KKThttp="http://localhost:50010/api.json"
headers={'Content-Type':'application/json'}

# читаем команду
fr=open('command.ini','r') 
sСommand=fr.read()
fr.close() 
        
print('***************************************************************************')
print('Читаем команду:')
sText=s99+'Дата старт: '+dt_string+' Читаем команду:'+sСommand+'\n'
print(sСommand)
print('***************************************************************************')

if sСommand == 'OpenSession' or sСommand == 'DobryiDen' :
    print("команда: "+sСommand)
    print('--------------------------------------------')
    
    textJSON='{"sessionKey": null, "command": "OpenSession", "portName": "COM3", "model": "185F"}'  # работает
    sText=sText+s99+'Команда:'+textJSON+'\n'
    
    print('Открываем сессию:\n')   
    r=requests.post(KKThttp, textJSON, headers=headers)

    print(r.text)
    sText=sText+'Ответ:'+r.text+'\n'
    
    print("r:\n{}\n".format(r))
    print("r.url:\n{}\n".format(r.url))                 #Посмотреть формат URL (с параметрами)
    print("r.headers:\n{}\n".format(r.headers))         #Header of the request
    print("r.status_code:\n{}\n".format(r.status_code)) #Получить код ответа
    print("r.text:\n{}\n".format(r.text))               #Text Output
    print("r.encoding:\n{}\n".format(r.encoding))       #Узнать, какую кодировку использует Requests
    print("r.content:\n{}\n".format(r.content))         #В бинарном виде
    print("r.json():\n{}\n".format(r.json()))           #JSON Output

    item = json.loads(r.text)
    sessionKey=item['sessionKey']
    result=item['result']
    print('--------------------------------------------')
    print('key:'+sessionKey)
    print('result:'+str(result))
    print('--------------------------------------------')

    dt_fin1 = datetime.datetime.now()
    tdelta = dt_fin1 - dt_start
    tsecs = tdelta.total_seconds()
    dt_delta = str(tsecs)
    sText=sText+s70+'Время выполнения Открыть Сессию: '+dt_delta+' сек.\n'+s70
          
    if result == 0:   # Если соединение прошло успешно 

        if sСommand == 'DobryiDen':            
            print('Проверяем статус ККТ:\n')
            print('--------------------------------------------')
            sText=sText+s70+'Проверяем статус ККТ:\n'
            textJSON='{"sessionKey": "'+sessionKey+'","command": "GetStatus"}';
            r=requests.post(KKThttp, textJSON, headers=headers)

            print(r.text)
            sText=sText+'Ответ:'+r.text+'\n'
            item = json.loads(r.text)

            isOpen = item['shiftInfo']['isOpen']
            sIsOpen = str(isOpen)

            print('--------------------------------------------')
            print(isOpen)
            print('--------------------------------------------')

            sText=sText+'**'+sIsOpen+'**'+'\n'

            dt_fin2 = datetime.datetime.now()
            tdelta = dt_fin2 - dt_fin1
            tsecs = tdelta.total_seconds()
            dt_delta = str(tsecs)
            sText=sText+s70+'Время выполнения Статус: '+dt_delta+' сек.\n'+s70
            
            #details = item['data']['details']

            #data = item['data']
            #if not 'details' in data:
            #    continue
            #details = data['details']

            if sIsOpen == 'False':
                sStrSmena='Смена закрыта!'
            else:
                sStrSmena='Смена открыта!'
                
            sText=sText+sStrSmena+'\n'
            
            sStr='Добрый день!\n'+sStrSmena
            textJSON='{"sessionKey": "'+sessionKey+'", "command": "PrintText", "text": "'+sStr+'" }'
            a_utf = textJSON.encode()
            r=requests.post(KKThttp, a_utf, headers=headers)

            dt_fin3 = datetime.datetime.now()
            tdelta = dt_fin3 - dt_fin2
            tsecs = tdelta.total_seconds()
            dt_delta = str(tsecs)
            sText=sText+s70+'Время выполнения Добрый день: '+dt_delta+' сек.\n'+s70  
        
        print('Закрываем сессию:\n')
        textJSON='{"sessionKey": "'+sessionKey+'", "command": "CloseSession"}'
        sText=sText+s70+'Команда:'+textJSON+'\n'
        
        r=requests.post(KKThttp, textJSON, headers=headers)

        print(r.text)
        sText=sText+'Ответ:'+r.text+'\n'+s70

        print("r:\n{}\n".format(r))
        print("r.url:\n{}\n".format(r.url))                 #Посмотреть формат URL (с параметрами)
        print("r.headers:\n{}\n".format(r.headers))         #Header of the request
        print("r.status_code:\n{}\n".format(r.status_code)) #Получить код ответа
        print("r.text:\n{}\n".format(r.text))               #Text Output
        print("r.encoding:\n{}\n".format(r.encoding))       #Узнать, какую кодировку использует Requests
        print("r.content:\n{}\n".format(r.content))         #В бинарном виде
        print("r.json():\n{}\n".format(r.json()))           #JSON Output
          
        print("\nСессия закрыта успешно!")
        print('--------------------------------------------')
    else:
        print("\nСесиия не открыта, закрыть не можем!\n")
        
else:
    print("неизвестная команда!")
    sText=sText+'Ответ: неизвестная команда:\n'+s70

dt_fin = datetime.datetime.now()
dt_string = dt_fin.strftime('%y/%m/%d %H:%M:%S')
tdelta = dt_fin - dt_start
tsecs = tdelta.total_seconds()
dt_string2 =  str (tsecs)
sText=sText+'Дата финиш: '+dt_string+' Время выполнения: '+dt_string2+' сек.\n'+s70

fw1=open('log_KKT_tot.txt','a+')
fw1.write(sText)
fw1.close()

fw1=open('log_KKT_.txt','w')
fw1.write(sText)
fw1.close()

