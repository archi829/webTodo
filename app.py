from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db = SQLAlchemy(app)  #initialize the db 

class Todo(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['con2id']  #pas in the id of wht u wanna take input of
        new_task = Todo(content=task_content)  #create a new task

        try:
            #push to database
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "ISsue happened"


    else:
        tasks = Todo.query.order_by(Todo.date_created).all()  #order all db items in the order they were created 
        return render_template('index.html', tasks = tasks)  #previous line wala variable


@app.route('/delete/<int:id>')  #id uniquely identifies the db entries
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)  

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Issue happened while deleting"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':  #if the form is submitted -> submit is clicked
        task.content = request.form['con2id']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Issue happened while updating"
    else:
        return render_template('update.html', task = task)


if __name__ == '__main__':
    app.run(debug=True)