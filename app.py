from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Tickit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemdesc = db.Column(db.String(200), nullable=False)
    itemdate = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Task %r>' % self.id 


@app.route('/')
def index():
        return render_template("index.html")

@app.route('/content', methods=['GET', 'POST'])
def content():  

        if request.method == 'POST':
            existingItems = Tickit.query.order_by(Tickit.itemdate).all()
            username = request.form['iusername']
            return render_template("content.html", uname=username, tasks=existingItems)
        else:
            #return "This is what other routes are seeing"
            existingItems = Tickit.query.order_by(Tickit.itemdate).all()
            username = "find"
            return render_template("content.html", uname=username, tasks=existingItems)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        itemDescription = request.form['useritem']
        itemObj = Tickit(itemdesc=itemDescription)
        try:
            db.session.add(itemObj)
            db.session.commit()  
            return redirect('/content')
        except:
            return "There was an issue adding the task to db"
    else:
        existingItems = Tickit.query.order_by(Tickit.itemdate).all() 
        username = "find"   
        return render_template("content.html", uname=username, tasks=existingItems, cross=200)


@app.route('/tick/<int:id>', methods=['GET', 'POST'])
def tick(id):
    if request.method == 'POST':
        task_to_tick = Tickit.query.get_or_404(id)
        existingItems = Tickit.query.order_by(Tickit.itemdate).all()    
        username = request.form['iusername']
        return render_template("content.html", uname=username, tasks=existingItems, cross=100)
    else:
        task_to_tick = Tickit.query.get_or_404(id)
        existingItems = Tickit.query.order_by(Tickit.itemdate).all()
        username = "find"    
        return render_template("content.html", uname=username, tasks=existingItems, cross=100)

@app.route('/untick/<int:id>', methods=['GET', 'POST'])
def untick(id):
    if request.method == 'POST':
        task_to_tick = Tickit.query.get_or_404(id)
        existingItems = Tickit.query.order_by(Tickit.itemdate).all()    
        username = request.form['iusername']
        return render_template("content.html", uname=username, tasks=existingItems, cross=200)
    else:
        task_to_tick = Tickit.query.get_or_404(id)
        existingItems = Tickit.query.order_by(Tickit.itemdate).all()  
        username = "find"  
        return render_template("content.html", uname=username, tasks=existingItems, cross=200)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method =='GET':
        task_to_edit = Tickit.query.get_or_404(id)
        try:

            return redirect('/content')
        except:
            return "There was a problem editing that task"
    else:
        return redirect('/content')

@app.route('/delete/<int:id>' , methods=['GET', 'POST'])
def delete(id):
    if request.method =='GET':
        task_to_delete = Tickit.query.get_or_404(id)
        try:
            db.session.delete(task_to_delete)
            db.session.commit() 
            return redirect('/content')
        except:
            return "There was a problem deleting that task"
    else:
        return redirect('/content')

if __name__ == "__main__":
    app.run(debug = True)
