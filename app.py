

from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    data =  db.Column(db.String(80), nullable=False)


    def __repr__(self):
        return '<Data %r>' % self.data + 'password %r' % self.password

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        email = session['email']
        return redirect(url_for('home',email=email))
    return render_template('login.html')

@app.route('/',methods=['POST','GET'])
def home():
    if 'email' in session:
        if request.method == 'POST':
            email = session['email']
            password = session['password']
            data = request.form['data']
            new_Data = Data(email=email,password=generate_password_hash(password) , data=data )
            db.session.add(new_Data)
            db.session.commit()
            return redirect('/')
        else:    
            email = session['email']
            data = Data.query.filter_by(email=email).all()
            return render_template('home.html',email=email,data=data,sessionn='email')
        
        
       


    return redirect(url_for('login'))


@app.route("/logout")
def logout():
    if "email" in session:
        session.pop("email",None)
        return redirect(url_for("login"))
    
    return redirect(url_for('login'))
       

@app.route('/delete/<int:id>')
def delete(id):
    data = Data.query.get_or_404(id)

    try:
        db.session.delete(data)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting data."


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    data = Data.query.get_or_404(id)

    if request.method == 'POST':
        data.data = request.form['name']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating data."

    else:
        title = "Update Data"
        return render_template('update.html', title=title, data=data)




if __name__ == "__main__":
    app.run(debug=True)

