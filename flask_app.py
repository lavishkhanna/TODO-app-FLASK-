# A BRIEF



# 'TASKMASTER' is a RESPONSIVE TODO application developed using flask framework, HTML and CSS

# The app revolves around three central tables: "Pending," "Ongoing," and "Completed," providing user with a clear overview of the progress and status of user tasks at a glance. By categorizing user tasks into these distinct stages, TaskMaster ensures that users have a well-structured and organized workflow.

# Update and delete functionalities are seamlessly integrated into TaskMaster, allowing users to easily modify and manage individual tasks as needed. Whether user need to make changes to task details, update their status, or completely remove them, the app provides users with the flexibility to adapt and refine user task list effortlessly.

# TaskTrackr is designed with a clean and minimalist aesthetic, prioritizing a distraction-free environment. The whitish background further enhances the app's minimalistic appeal, allowing users to focus on their tasks without unnecessary visual clutter. The user interface is optimized for a seamless experience, ensuring smooth navigation and effortless interaction.

# Hence the minimilaist simple CSS







# IMPORTING REQUIRED PACKAGES

from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



# DECLARING OUR MAIN APP
app = Flask(__name__)


# SETTING SEPARATE DATABASES FOR EACH TASK
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo-2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# USING BINDS TO INTEGRATE ONGOING AND COMPLETED DATABASE ALSO
app.config['SQLALCHEMY_BINDS']={ 'ongo':  'sqlite:///ongo_db.db', 'comp':  'sqlite:///comp_db.db'}

with app.app_context():
    db=SQLAlchemy(app)


# DATABASE FOR RECORDING PENDING TASKS

class Tpend(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(1000),nullable=False)
    
    date_time=db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"

# DATABASE FOR RECORDING ONGOING TASKS

class Tongo(db.Model):
    
    __bind_key__='ongo'
    
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(1000),nullable=False)
    
    date_time=db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"
    
# DATABASE FOR RECORDING COMPLETED TASKS    

class Tcomp(db.Model):
    
    __bind_key__='comp'
    
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(1000),nullable=False)
    
    date_time=db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"
    
    
# <--------------------------------------------MAJOR TABLE PAGES OF OUR APP------------------------------------------------------------------>
    
@app.route('/')
def c():
    return redirect('/pending')
    
# pending page for documenting pending tasks 
    
@app.route('/pending', methods=['GET','POST'])
def pending():
    
    if request.method=='POST':
        
        ptitle=request.form['title']
        pdesc=request.form['desc']
        
        cat=request.form['score']
        
        todo_p=Tpend(title=ptitle,desc=pdesc)
        db.session.add(todo_p)
        db.session.commit()
    
    all_todo=Tpend.query.all()
    print(all_todo)
    print(Tpend.query.count())
    total=Tpend.query.count()
    total_p=Tpend.query.count()
    total_o=Tongo.query.count()
    total_c=Tcomp.query.count()
    
    return render_template('pend.html',all_todo=all_todo,total_p=total_p,total_o=total_o,total_c=total_c)

# ONGOING PAGE FOR DOCUMENTING ONGOING TASKS

@app.route('/ongoing', methods=['GET','POST'])
def ongoing():
    
    if request.method=='POST':
        
        ptitle=request.form['title']
        pdesc=request.form['desc']
        
        cat=request.form['score']
        
        todo_p=Tongo(title=ptitle,desc=pdesc)
        db.session.add(todo_p)
        db.session.commit()
    
    all_todo=Tongo.query.all()
    print(all_todo)
    print(Tongo.query.count())
    
    total=Tongo.query.count()
    total_p=Tpend.query.count()
    total_o=Tongo.query.count()
    total_c=Tcomp.query.count()
    
    return render_template('ongo.html',all_todo=all_todo,total_p=total_p,total_o=total_o,total_c=total_c)
    

# COMPLETED PAGE FOR DOCUMENTING ONGOING TASKS

@app.route('/completed', methods=['GET','POST'])
def completed():
    
    name='rst'
    if request.method=='POST':
        
        ptitle=request.form['title']
        pdesc=request.form['desc']
        
        cat=request.form['score']
        name=cat
        
        todo_p=Tcomp(title=ptitle,desc=pdesc)
        db.session.add(todo_p)
        db.session.commit()
    
    all_todo=Tcomp.query.all()
    print(all_todo)
    print(Tcomp.query.count())
    
    total=Tcomp.query.count()
    total_p=Tpend.query.count()
    total_o=Tongo.query.count()
    total_c=Tcomp.query.count()
    
    
    return render_template('comp.html',all_todo=all_todo,name=name,total_p=total_p,total_o=total_o,total_c=total_c)

# <----------------------------------------------------ACCESSIBLE FEATURES FOR TASKS---------------------------------------------------------->

# TO DELETE UNWANTED TASKS

@app.route('/delete_pend/<int:sno>')
def delete_pend(sno):
    todo=Tpend.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/pending')

@app.route('/delete_comp/<int:sno><string:name>')
def delete_comp(sno,name):
    print(name)
    todo=Tcomp.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/completed')

@app.route('/delete_ongo/<int:sno><string:name>')
def delete_ongo(sno,name):
    print(name)
    todo=Tongo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/ongoing')


# TO UPDATE TASKS WITH WRONG DOCUMENTATION

@app.route('/update_pend/<int:sno>', methods=['GET','POST'])
def upd_pend(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Tpend.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/pending')
    
    todo=Tpend.query.filter_by(sno=sno).first()
    return render_template('up_pend.html',todo=todo)

@app.route('/update_ongo/<int:sno>', methods=['GET','POST'])
def upd_ongo(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Tongo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/ongoing')
    
    todo=Tongo.query.filter_by(sno=sno).first()
    return render_template('up_ongo.html',todo=todo)

@app.route('/update_comp/<int:sno>', methods=['GET','POST'])
def upd_comp(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Tcomp.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/completed')
    
    todo=Tcomp.query.filter_by(sno=sno).first()
    return render_template('up_comp.html',todo=todo)




# TO RUN OUR MAIN APP
if __name__=='__main__':
    app.run(debug=True,port='8000')