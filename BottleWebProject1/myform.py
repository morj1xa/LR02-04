from asyncio.windows_events import NULL
from bottle import post, request
import re
from datetime import datetime
import pdb
import os
import json

@post('/home', method='post')
def my_form():
    quest = request.forms.get('QUEST')
    mail = request.forms.get('ADRESS')
    username = request.forms.get('USERNAME')
    #pattern = re.compile(r"^\S+@\S+\.\S+$")
    
    if mail == "" or username == "" or quest == "":
        return "All forms must be filled"
    else:
        if mailCheck(mail):
            curdate = datetime.now()
            # �������� ���������� ���� � �������� ��������
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # ������� ���������� ���� � ����� JSON � ������� ��������
            json_file = os.path.join(current_dir, 'json_data.json')

            # ���������, ���������� �� ���� JSON, ���� ��� - ������� ���
            if not os.path.exists(json_file):
                with open(json_file, 'w') as new_json:
                    new_json.write('{}')

            # ��������� ���� JSON � ��������� ��� ����������
            with open(json_file, 'r') as read_json:
                questions = json.load(read_json)

            # ��������� ����� ������ � ����� � �������
            if mail in questions:
                questions[mail].append(quest) 
            else:
                questions[mail] = [quest]

            # ���������� ����������� ������ � ���� JSON
            with open(json_file, 'w') as write_json:
                json.dump(questions, write_json)
        
            return "Thanks, "+username+"! The answer will be sent to the mail %s" % mail + f" |  Access Date: {curdate}"
        else:
            return "Dear, "+username+"! You have entered an incorrect email!"
    

def mailCheck(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))