import os, random
from app import app
from flask import render_template, request, redirect
import users, messages
from werkzeug.utils import secure_filename

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Käyttäjätunnus tai salasana on väärä")
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
        
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 50:
            return render_template("error.html", message="Tunnuksessa tulee olla 1-50 merkkiä")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if password1 == "":
            return render_template("error.html", message="Salasana on tyhjä")

        role = request.form["role"]
        if role not in ("1", "2"):
            return render_template("error.html", message="Käyttäjäroolia ei ole olemassa")

        if not users.register(username, password1, role):
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
        return redirect("/")

@app.route("/add_thread", methods=["POST"])
def add_thread():
    board_name = request.form["board"]

    title = request.form["title"]
    if len(title) < 1 or len(title) > 50:
        return render_template("error.html", message="Otsikossa tulee olla 1-50 merkkiä")

    message = request.form["message"]
    if len(message) < 1 or len(message) > 1500:
        return render_template("error.html", message="Viestissä tulee olla 1-1500 merkkiä")
        
    file = request.files["file"]
    image_file_name = secure_filename(file.filename)
    newfilename = str(random.randint(10000000,100000000))+"."+image_file_name.rsplit(".", 1)[1].lower()
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], newfilename))
    image_file = "static/images/"+str(newfilename)

    if not messages.add_thread(image_file, image_file_name, title, message, board_name):
        return render_template("error.html", message="Viestin lähettäminen ei onnistunut")
    return redirect("/"+str(board_name))

@app.route("/remove", methods=["GET", "POST"])
def remove_thread():
    users.require_role(2)

    if request.method == "GET":
        return render_template("remove.html")

    if request.method == "POST":
        users.check_csrf()
        thread_id = request.form["thread_id"]
        messages.remove_thread(thread_id)
    return redirect("/")

@app.route("/add_reply", methods=["GET", "POST"])
def add_reply():
    if request.method == "GET":
        return render_template("reply.html")

    if request.method == "POST":
        users.check_csrf()
        
        thread_id = request.form["thread_id"]

        title = request.form["title"]
        if len(title) > 50:
            return render_template("error.html", message="Otsikossa tulee olla enintään 50 merkkiä")

        message = request.form["message"]
        if len(message) > 1500:
            return render_template("error.html", message="Viestissä tulee olla enintään 1500 merkkiä")
        
        file = request.files["file"]
        image_file_name = secure_filename(file.filename)
        newfilename = str(random.randint(10000000,100000000))+"."+image_file_name.rsplit(".", 1)[1].lower()
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], newfilename))
        image_file = "static/images/"+str(newfilename)

        if not messages.add_reply(image_file, image_file_name, title, message, thread_id):
            return render_template("error.html", message="Viestin lähettäminen ei onnistunut")
        return redirect("reply/"+str(thread_id))

@app.route("/reply/<thread_id>")
def reply(thread_id):
    count = messages.reply_count(thread_id)
    first_thread=messages.show_thread(thread_id)
    return render_template("reply.html", id=thread_id, first_thread=first_thread, replies=messages.show_all_replies(thread_id), count=count)

@app.route("/philosophy", methods=["GET"])
def philosophy():
    board_name = "philosophy"
    return render_template("philosophy.html", threads=messages.show_all_threads(board_name))

@app.route("/history", methods=["GET"])
def history():
    board_name = "history"
    return render_template("history.html", threads=messages.show_all_threads(board_name))

@app.route("/languages", methods=["GET"])
def languages():
    board_name = "languages"
    return render_template("languages.html", threads=messages.show_all_threads(board_name))

@app.route("/anthropology", methods=["GET"])
def anthropology():
    board_name = "anthropology"
    return render_template("anthropology.html", threads=messages.show_all_threads(board_name))

@app.route("/theology", methods=["GET"])
def theology():
    board_name = "theology"
    return render_template("theology.html", threads=messages.show_all_threads(board_name))

@app.route("/law", methods=["GET"])
def law():
    board_name = "law"
    return render_template("law.html", threads=messages.show_all_threads(board_name))

@app.route("/edu", methods=["GET"])
def edu():
    board_name = "edu"
    return render_template("edu.html", threads=messages.show_all_threads(board_name))

@app.route("/pol", methods=["GET"])
def pol():
    board_name = "pol"
    return render_template("pol.html", threads=messages.show_all_threads(board_name))

@app.route("/econ", methods=["GET"])
def econ():
    board_name = "econ"
    return render_template("econ.html", threads=messages.show_all_threads(board_name))

@app.route("/math", methods=["GET"])
def math():
    board_name = "math"
    return render_template("math.html", threads=messages.show_all_threads(board_name))

@app.route("/physics", methods=["GET"])
def physics():
    board_name = "physics"
    return render_template("physics.html", threads=messages.show_all_threads(board_name))

@app.route("/chemistry", methods=["GET"])
def chemistry():
    board_name = "chemistry"
    return render_template("chemistry.html", threads=messages.show_all_threads(board_name))

@app.route("/cs", methods=["GET"])
def cs():
    board_name = "cs"
    return render_template("cs.html", threads=messages.show_all_threads(board_name))

@app.route("/geology", methods=["GET"])
def geology():
    board_name = "geology"
    return render_template("geology.html", threads=messages.show_all_threads(board_name))

@app.route("/geography", methods=["GET"])
def geography():
    board_name = "geography"
    return render_template("geography.html", threads=messages.show_all_threads(board_name))

@app.route("/med", methods=["GET"])
def med():
    board_name = "med"
    return render_template("med.html", threads=messages.show_all_threads(board_name))

@app.route("/dentistry", methods=["GET"])
def dentistry():
    board_name = "dentistry"
    return render_template("dentistry.html", threads=messages.show_all_threads(board_name))

@app.route("/slp", methods=["GET"])
def slp():
    board_name = "slp"
    return render_template("slp.html", threads=messages.show_all_threads(board_name))

@app.route("/psy", methods=["GET"])
def psy():
    board_name = "psy"
    return render_template("psy.html", threads=messages.show_all_threads(board_name))

@app.route("/animalmed", methods=["GET"])
def animalmed():
    board_name = "animalmed"
    return render_template("animalmed.html", threads=messages.show_all_threads(board_name))

@app.route("/pharma", methods=["GET"])
def pharma():
    board_name = "pharma"
    return render_template("pharma.html", threads=messages.show_all_threads(board_name))

@app.route("/forest", methods=["GET"])
def forest():
    board_name = "forest"
    return render_template("forest.html", threads=messages.show_all_threads(board_name))

@app.route("/agri", methods=["GET"])
def agri():
    board_name = "agri"
    return render_template("agri.html", threads=messages.show_all_threads(board_name))
