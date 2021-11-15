from flask import Flask
from flask import render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kanbanDatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Kanban(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), default='To do')
    content = db.Column(db.String(500), nullable=False)
    timeStamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __str__(self):
        return 'object with {} status created'.format(self.status)

    
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task = request.form['input-content']
        stat = request.form['select-content']
        if task == '' and stat == 'Status':
            return 'task and stat fields should not be left empty'
        new_task = Kanban(content=task, status=stat)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was problem adding the task'
    else:
        tasks = Kanban.query.order_by(Kanban.timeStamp.desc()).all()
        countT = Kanban.query.filter(Kanban.status.contains("To do")).count()
        countP = Kanban.query.filter(Kanban.status.contains("In Progress")).count()
        countC = Kanban.query.filter(Kanban.status.contains("Completed")).count()
        return render_template('TIC.html', tasks=tasks, countT=countT, countP=countP, countC=countC)
    
@app.route('/delete/<int:id>')
def delete(id):
    item_to_delete = Kanban.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'The task could not be deleted'
    
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task_to_edit = Kanban.query.get_or_404(id)
    if request.method == 'POST':
        task_to_edit.content = request.form['edit-content']
        task_to_edit.status = request.form['select-content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'The task could not be edited'
    else:
        tasks = Kanban.query.order_by(Kanban.timeStamp.desc()).all()
        countT = Kanban.query.filter(Kanban.status.contains("To do")).count()
        countP = Kanban.query.filter(Kanban.status.contains("In Progress")).count()
        countC = Kanban.query.filter(Kanban.status.contains("Completed")).count()
        return render_template('edit.html', task=task_to_edit, tasks=tasks, countT=countT, countP=countP, countC=countC)
        