from flask import Flask,render_template,flash,redirect,url_for,session,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/kskn1/Desktop/Web/ucn-master/ucnmachine1.db"
app.config["SECRET_KEY"] = "abc"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.init_app(app)

class Drawings(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    describe = db.Column(db.String(200))
    category = db.Column(db.String(20))
    hours_drawed = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, default=func.current_timestamp())
    show_features = db.Column(db.Boolean, default=False)
    show_popular = db.Column(db.Boolean, default=False)
    image_path = db.Column(db.String(255), nullable=False)
    carousel_img1 = db.Column(db.String(255))
    carousel_img2 = db.Column(db.String(255))
    carousel_img3 = db.Column(db.String(255))

class DeletedDrawings(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    describe = db.Column(db.String(200))
    category = db.Column(db.String(20))
    hours_drawed = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, default=func.current_timestamp())
    show_features = db.Column(db.Boolean, default=False)
    show_popular = db.Column(db.Boolean, default=False)
    image_path = db.Column(db.String(255), nullable=False)
    carousel_img1 = db.Column(db.String(255))
    carousel_img2 = db.Column(db.String(255))
    carousel_img3 = db.Column(db.String(255))

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)



db.init_app(app)

@app.route("/")
def index():
    drawings = Drawings.query.all()
    return render_template("index.html", drawings = drawings)

@app.route("/explore", methods = ["GET", "POST"])
def explore():
    drawings = Drawings.query.all()
    return render_template("explore.html", drawings = drawings)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/addDrawings", methods=["GET", "POST"])
def addDrawing():
    if request.method == "POST":
        title = request.form.get("title")
        describe = request.form.get("describe")
        category = request.form.get("category")
        hours_drawed = request.form.get("hours_drawed")
        show_features = request.form.get("show_features") == 'on'
        show_popular = request.form.get("show_popular") == 'on'

        uploaded_file = request.files['file']
        uploaded_carousel1 = request.files['carousel_img1']
        uploaded_carousel2 = request.files['carousel_img2']
        uploaded_carousel3 = request.files['carousel_img3']

        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            filename_c1 = secure_filename(uploaded_carousel1.filename)
            filename_c2 = secure_filename(uploaded_carousel2.filename)
            filename_c3 = secure_filename(uploaded_carousel3.filename)

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file_path1 = os.path.join(app.config['UPLOAD_FOLDER'], filename_c1)
            file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename_c2)
            file_path3 = os.path.join(app.config['UPLOAD_FOLDER'], filename_c3)
            
            uploaded_file.save(file_path)
            uploaded_carousel1.save(file_path1)
            uploaded_carousel2.save(file_path2)
            uploaded_carousel3.save(file_path3)

            

            newDrawing = Drawings(
                title=title,
                describe=describe,
                category=category,
                hours_drawed=hours_drawed,
                show_features=show_features,
                show_popular=show_popular,
                image_path=file_path,
                carousel_img1=file_path1,
                carousel_img2=file_path2,
                carousel_img3=file_path3
            )

            db.session.add(newDrawing)
            db.session.commit()
            return redirect(url_for('index'))

    return render_template("addDrawings.html")

@app.route("/drawingList", methods= ["GET", "POST"])
def drawingList():
    drawings = Drawings.query.all()
    return render_template("drawinglist.html", drawings = drawings)


@app.route('/delete/<int:drawing_id>')
def deleteDrawing(drawing_id):
    drawing = Drawings.query.get(drawing_id)

    deleted_drawing = DeletedDrawings(
            title = drawing.title,
            describe = drawing.describe,
            category = drawing.category,
            created_date = drawing.created_date,
            hours_drawed = drawing.hours_drawed,
            show_features = drawing.show_features,
            show_popular = drawing.show_popular,
            image_path = drawing.image_path,
            carousel_img1 = drawing.carousel_img1,
            carousel_img2 = drawing.carousel_img2,
            carousel_img3 = drawing.carousel_img3
        )

    db.session.add(deleted_drawing)
    db.session.delete(drawing)
    db.session.commit()
    return redirect(url_for('drawingList'))

@app.route('/deleteK/<int:drawing_id>')
def deleteK(drawing_id):
    drawing = DeletedDrawings.query.get(drawing_id)
    db.session.delete(drawing)
    db.session.commit()
    return redirect(url_for('deletedList'))

@app.route('/restore/<int:drawing_id>')
def restore(drawing_id):
    drawing = DeletedDrawings.query.get(drawing_id)
    restored_drawing = Drawings(
        title = drawing.title,
        describe = drawing.describe,
        category = drawing.category,
        created_date = drawing.created_date,
        hours_drawed = drawing.hours_drawed,
        show_features = drawing.show_features,
        show_popular = drawing.show_popular,
        image_path = drawing.image_path,
        carousel_img1 = drawing.carousel_img1,
        carousel_img2 = drawing.carousel_img2,
        carousel_img3 = drawing.carousel_img3
    )
    db.session.add(restored_drawing)
    db.session.delete(drawing)
    db.session.commit()
    return redirect(url_for('deletedList'))

@app.route('/deletedList', methods= ["GET", "POST"])
def deletedList():
    deleted_drawings = DeletedDrawings.query.all()
    return render_template("/deletedList.html", deleted_drawings = deleted_drawings)

@app.route('/update/<int:drawing_id>', methods = ["GET", "POST"])
def updateDrawing(drawing_id):
    drawing = Drawings.query.get(drawing_id)

    if request.method == "POST":
        drawing.title = request.form.get("title")
        drawing.describe = request.form.get("describe")
        drawing.category = request.form.get("category")
        drawing.hours_drawed = request.form.get("hours_drawed")
        drawing.show_features = request.form.get("show_features") == 'on'
        drawing.show_popular = request.form.get("show_popular") == 'on'

        uploaded_file = request.files['file']
        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(file_path)
            drawing.image_path=file_path
        else: print("Error")

        db.session.commit()
        return redirect(url_for("drawingList"))

    return render_template("update.html", drawing = drawing)


@app.route('/details/<int:drawing_id>')
def details(drawing_id):
    drawing = Drawings.query.get(drawing_id)
    files_list = [drawing.carousel_img1,drawing.carousel_img2 ,drawing.carousel_img3]
    list_for_count = [s for s in files_list if s != None]
    length = len(list_for_count)+1

    return render_template("details.html", drawing = drawing, length = length)


@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            session['logged_in'] = True
            return redirect(url_for("index"))

    return render_template("login.html")
    
@app.route("/logout")
def logout():
    logout_user()
    session['logged_in'] = False
    return redirect(url_for("index"))


@login_required
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)



