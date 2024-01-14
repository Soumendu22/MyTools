from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import string


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        
    allTodo = Todo.query.all() 
    return render_template('todo.html', allTodo=allTodo)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/todo")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/todo")

@app.route('/password')
def password():
    return render_template('password.html')

@app.route('/genpassword',methods=['GET','POST'])
def genpassword():
    minpasslen = 5
    maxpasslen = 30

    passlen = int(request.form.get('passlen'))



    include_spaces = request.form.get('includespaces')
    include_numbers = request.form.get('includenumbers')
    include_special_chars = request.form.get('includespecialchars')
    include_uppercase_letters= request.form.get('includeuppercaseletters')
    
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    special_chars = string.punctuation

    print(include_spaces,include_numbers,include_special_chars,include_uppercase_letters)

    char_sets = [lowercase_letters]

    if include_spaces=='on':
        char_sets.append(' ')
    if include_numbers=='on':
        char_sets.append(digits)
    if include_special_chars=='on':
        char_sets.append(special_chars)
    if include_uppercase_letters=='on':
        char_sets.append(uppercase_letters)
    all_chars = ''.join(char_sets)
    password = random.choices(all_chars, k=passlen)
    password = ''.join(password)
    return render_template('password.html',generatedpassword=password)

def replace_multiple_newlines(text):
    lines = text.split('\n')
    lines = [line for line in lines if line.strip()]
    return len(lines)

@app.route('/count')
def count():
    return render_template('count.html') 

@app.route('/word',methods=['GET','POST'])
def word():
    text = request.form['text']
    
    words = len(text.split())
    
    paras = replace_multiple_newlines(text)
    text = text.replace('\r','')
    text = text.replace('\n','')
    chars = len(text)
    return render_template('count.html',words=words,chars=chars)

if __name__ == "__main__":
    app.run(debug=True, port=5000)