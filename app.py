from flask import Flask, render_template
from flask import request, redirect, abort
import os

app = Flask(__name__, static_folder='static')
members = [{"id":"sookbun", "pw":"111111"},
           {"id":"jeehye", "pw":"222222"}]


def get_template(filename):
    with open('views/'+filename, 'r', encoding="utf-8") as f:
        template = f.read()
    return template

def get_menu():
    menu = [e for e in os.listdir('content') if e[0] !='.']
    menu_temp = "<li><a href='/{0}?id={1}'>{0}</a></li>"
    return "\n".join([menu_temp.format(m,request.args.get('id')) for m in menu])


@app.route('/')
def index():
    #views/index.html에서 파일을 받아오자
    id = request.args.get('id', '')
    #get default값은 NONE이기 때문에 이상한 문자열 출력 방지를 위해 ''라고 NONE일때 치환한다라고 작성

    
    title = 'Welcome '
    content = 'Welcome...' + id
    menu = get_menu()
#     print("*" * 100)
#     print(id)
    if id == '':
        template = get_template('template_default.html')
        return template.format(title, content, menu, " ")
    else:
        template = get_template('template.html')
        
        return redirect("/main?id="+id)

@app.route("/main")
def main():
    id = request.args.get('id', '')
    title = 'Welcome '
    content = 'Welcome...' + id
    menu = get_menu()
    template = get_template('template.html')
    image_file ='<img src="/static/starisborn.jpg" alt="main" width="50%">'
    return template.format(title, content, menu, image_file, id) 
    
@app.route('/<title>')
def html(title):
    id = request.args.get('id', '')
    params ={'id': id}

    #views/index.html에서 파일을 받아오자
    template = get_template('template.html')
    menu = get_menu()
    with open(f'content/{title}', 'r') as f:
        content = f.read()
    lylics=str(content.split('*')[0])[7:].replace("\n","<br>").replace("<br><br>","<br>")
    url = str(content.split('*')[1])[4:]
 
    return template.format(title, lylics, menu, url, id)



@app.route('/login', methods=['GET', 'POST'])
def login():
 
    login = get_template('login.html')
    menu = get_menu()
    if request.method == 'GET':
        return login.format("", "",menu,"")
    elif request.method == 'POST':
        #만약 회원이 아니면, "회원이 아닙니다."라고 알려주자
        m = [e for e in members if e['id']==request.form['id']]
        if len(m) ==0:
            return login.format("<p>회원이 아닙니다.</p>","", menu)
        #만약 패스워드가 다르면, "패스워드를 확인해 주세요"라고 알려주자
        if request.form['pw'] != m[0]['pw']:
            return login.format("<p>패스워드를 확인해 주세요</p>","", menu)
        
        #로그인 성공시에는 메인으로
        return redirect("/?id=" +m[0]['id'])

@app.route('/create', methods=['GET', 'POST'])
def create():
    template = get_template('create.html')
    menu = get_menu()
    id = request.args.get('id', '')
    if request.method == 'GET':
        return template.format("", "", menu, "", id)
    elif request.method == 'POST':
        with open(f'content/{request.form["title"]}', 'w') as f:         
            f.write(f"lylics: {request.form['desc']}"+'*'+'url:'+request.form['url'])
        return redirect("/main?id="+id)
    

@app.route("/delete/<title>")
def delete(title):
    template_main = get_template('template.html')
    menu = get_menu()
    menu_list = [e for e in os.listdir('content') if e[0] !='.']
    id = request.args.get('id', '')
    if title in menu_list:
        os.remove(f"content/{title}")
        return redirect("/main?id="+id)
    else:
        lylics = "왼쪽 곡 리스트 중에서 하나 선택해주세요"
        return template_main.format(title,  lylics, menu, "",id)
   


@app.route("/favicon.ico")
def favicon():
    return abort(404)

@app.route('/update/<title>', methods=['GET', 'POST'])
def update(title):
    template = get_template('update.html')
    template_main = get_template('template.html')
    menu = get_menu()
    menu_list = [e for e in os.listdir('content') if e[0] !='.']
    id = request.args.get('id', '')
    if request.method == 'GET':
      
            if title in menu_list:
                with open(f'content/{title}','r') as f:
                    content = f.read()
                    lylics=str(content.split('*')[0])[7:]
                    url = str(content.split('*')[1])[4:]
                return template.format(title, lylics, menu, url, id)
            else:
                lylics = "왼쪽 곡 리스트 중에서 하나 선택해주세요"
                return template_main.format(title,  lylics, menu, "", id)
        
    
    elif request.method == 'POST':
        with open(f'content/{request.form["title"]}','w') as f:
             f.write('lylics:'+request.form['desc']+'*'+'url:'+request.form['url'])
        return redirect(f'/{request.form["title"]}?id={id}')
 
        
        
