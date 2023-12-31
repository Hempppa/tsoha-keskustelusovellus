import secrets
from flask import redirect, render_template, request, session, abort
import readdb
import writedb
from app import app, owner

#Käyttäjän luonti ja kirjautuminen
#User creation and login

#obselete
@app.route("/account")
def account(error=False, error_msg=""):
    try:
        is_admin = readdb.is_admin(session["username"])
    except:
        is_admin = False
    areas = readdb.get_areas()
    return render_template("account.html", error=error, error_msg=error_msg, areas=areas, is_admin=is_admin)

#obselete
@app.route("/newaccount")
def new_account(error=False, error_msg=""):
    try:
        is_admin = readdb.is_admin(session["username"])
    except:
        is_admin = False
    areas = readdb.get_areas()
    return render_template("newaccount.html", error=error, error_msg=error_msg, areas=areas, is_admin=is_admin)

#obselete
@app.route("/create", methods=["POST"])
def create():
    name = request.form["accname"]
    password = request.form["passwrd"]
    if not password or not name:
        return new_account(True, "Nimi tai salasanakenttä tyhjä")
    #Tähän sitten salasanan laatutarkastus
    #elif (len(password) < 8) or (name in password):
    #
    if writedb.add_user(name, password):
        session["username"] = name
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")
    return new_account(True, "Käyttäjänimi varattu")

@app.route("/login", methods=["POST"])
def login():
    if request.form["submit"] == "Kirjaudu":
        name = request.form["accname"]
        password = request.form["passwrd"]
        if readdb.confirm_user_pass(name, password):
            session["username"] = name
            session["csrf_token"] = secrets.token_hex(16)
            return redirect(request.form["current_url"])
        return index(error=True, error_msg="Nimi tai salasana väärin")
    else:
        name = request.form["accname"]
        password = request.form["passwrd"]
        if not password or not name:
            return index(True, "Nimi tai salasanakenttä tyhjä")
        #Tähän sitten salasanan laatutarkastus
        #elif (len(password) < 8) or (name in password):
        #
        if writedb.add_user(name, password):
            session["username"] = name
            session["csrf_token"] = secrets.token_hex(16)
            return redirect(request.form["current_url"])
        return index(error=True, error_msg="Käyttäjänimi varattu")


#Uloskirjautuminen ja käyttäjän poistaminen
#Logout and user removal


@app.route("/logout")
def logout():
    del session["username"]
    del session["csrf_token"]
    return redirect("/")

@app.route("/changepass")
def change_pass(error=False, error_msg=""):
    try:
        is_admin = readdb.is_admin(session["username"])
    except:
        is_admin = False
    areas = readdb.get_areas()
    return render_template("changepass.html", error=error, error_msg=error_msg, areas=areas, is_admin=is_admin)

@app.route("/changepass/confirm", methods=["POST"])
def change_confirm():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if readdb.confirm_user_pass(session["username"], request.form["oldpasswrd"]) and not request.form["newpasswrd"]:
        writedb.change_user_pass(session["username"], request.form["newpasswrd"])
        return redirect("/personal")
    return change_pass(True, "väärä salasana")

@app.route("/rmvuser")
def rmv_user(error=False, error_msg=""):
    try:
        is_admin = readdb.is_admin(session["username"])
    except:
        is_admin = False
    areas = readdb.get_areas()
    return render_template("rmvuser.html", error=error, error_msg=error_msg, areas=areas, is_admin=is_admin)

@app.route("/rmvuser/confirm", methods=["POST"])
def rmv_confirm():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if readdb.confirm_user_pass(request.form["accname"], request.form["passwrd"]):
        if session["username"] == request.form["accname"]:
            writedb.delete_user(session["username"])
            del session["username"]
            return redirect("/")
    return rmv_user(error=True, error_msg="Käyttäjänimi tai salasana väärin")


#Käyttäjäkohtaiset
#User oriented stuff


@app.route("/personal")
def personal(msg=False, msg_content=""):
    try:
        is_admin = readdb.is_admin(session["username"])
    except:
        is_admin = False
    areas = readdb.get_areas()
    return render_template("personal.html", msg=msg, msg_content=msg_content, owner=owner, areas=areas, is_admin=is_admin)

@app.route("/started")
def started():
    try:
        is_admin = readdb.is_admin(session["username"])
    except:
        is_admin = False
    areas = readdb.get_areas()
    discussions = readdb.get_discussion_by_writer(session["username"])
    return render_template("personaldiscussions.html", discussions=discussions, areas=areas, is_admin=is_admin)

@app.route("/addadmin")
def add_admin(error=False, error_msg=""):
    try:
        is_admin = readdb.is_admin(session["username"])
    except:
        is_admin = False
    areas = readdb.get_areas()
    if session["username"] != owner:
        abort(403)
    return render_template("addadmin.html", error=error, error_msg=error_msg, areas=areas, is_admin=is_admin)

@app.route("/addadmin/confirm", methods=["POST"])
def confirm_add_admin():
    if session["csrf_token"] != request.form["csrf_token"] or session["username"] != owner:
        abort(403)
    if not request.form["username"]:
        return add_admin(error=True, error_msg="Nimikenttä tyhjä")
    if request.form["submit"] == "Lisää admin":
        writedb.add_admin(request.form["username"])
    else:
        writedb.remove_admin(request.form["username"])
    return redirect("/addadmin")


#Kaverilista
#Friendlist


@app.route("/friendlist")
def friends(req=False, req_msg=""):
    try:
        is_admin = readdb.is_admin(session["username"])
    except:
        is_admin = False
    areas = readdb.get_areas()
    friendlist = readdb.get_friends_by_user(session["username"])
    return render_template("friendlist.html", friends=friendlist, request=req, req_msg=req_msg, areas=areas, is_admin=is_admin)

@app.route("/friendlist/send")
def friend_send(req=False, req_msg=""):
    try:
        is_admin = readdb.is_admin(session["username"])
    except:
        is_admin = False
    areas = readdb.get_areas()
    return render_template("friendsend.html", request=req, req_msg=req_msg, areas=areas, is_admin=is_admin)

@app.route("/friendlist/send/confirm", methods=["POST"])
def send_friend():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if readdb.check_user_exist(request.form["friend"]):
        writedb.add_friend(session["username"], request.form["friend"])
        return friends(True, "Kaverikutsu lähetetty")
    return friend_send(True, "Käyttäjää ei löydy")

@app.route("/friendlist/received")
def sent_requests():
    try:
        is_admin = readdb.is_admin(session["username"])
    except:
        is_admin = False
    areas = readdb.get_areas()
    requested = readdb.get_friend_requests(session["username"])
    return render_template("requests.html", requested=requested, areas=areas, is_admin=is_admin)

@app.route("/friendlist/accept", methods=["POST"])
def accept_requests():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    writedb.add_friend(session["username"],request.form["username"])
    return redirect("/friendlist/received")

@app.route("/friendlist/reject", methods=["POST"])
def reject_requests():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    writedb.remove_friend(request.form["username"],session["username"])
    return redirect("/friendlist/received")


#Direct message


@app.route("/friendlist/dm", methods=["POST"])
def directmessage():
    try:
        is_admin = readdb.is_admin(session["username"])
    except:
        is_admin = False
    areas = readdb.get_areas()
    if not readdb.check_friend(session["username"], request.form["username"]):
        abort(403)
    messages = readdb.get_directmessages(session["username"], request.form["username"])
    return render_template("directmessage.html", messages=messages, friend=request.form["username"], areas=areas, is_admin=is_admin)

@app.route("/friendlist/dm/msg-delete<int:id1>", methods=["POST"])
def dm_msg_delete(id1):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if readdb.get_directmessage_by_id(id1).user1 == session["username"]:
        writedb.delete_directmessage(id1)
        return redirect("/friendlist/dm", code=307)
    abort(403)

@app.route("/friendlist/dm/newmessage", methods=["POST"])
def new_directmessage():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if not readdb.check_friend(session["username"], request.form["username"]):
        abort(403)
    message = request.form["bodyfield"]
    writedb.add_directmessage(session["username"], request.form["username"], message)
    return redirect("/friendlist/dm", code=307)


#hakutoiminnot
#search functionality


@app.route("/search")
def search():
    try:
        is_admin = readdb.is_admin(session["username"])
    except:
        is_admin = False
    areas = readdb.get_areas()
    discussions = readdb.get_discussion_by_search(request.args["query"], None)
    return render_template("search.html", query=request.args["query"], discussions=discussions, id1=None, areas=areas, is_admin=is_admin)

@app.route("/area/<int:id1>/search")
def area_search(id1):
    try:
        is_admin = readdb.is_admin(session["username"])
    except:
        is_admin = False
    areas = readdb.get_areas()
    discussions = readdb.get_discussion_by_search(request.args["query"], id1)
    print(discussions)
    return render_template("search.html", query=request.args["query"], discussions=discussions, id1=id1, areas=areas, is_admin=is_admin)

@app.route("/area/<int:id1>/discussion/<int:id2>/search")
def discussion_search(id1, id2):
    try:
        is_admin = readdb.is_admin(session["username"])
    except:
        is_admin = False
    areas = readdb.get_areas()
    messages = readdb.get_message_by_search(request.args["query"], id2)
    return render_template("messagesearch.html", query=request.args["query"], messages=messages, ids=[id1, id2], areas=areas, is_admin=is_admin)

@app.route("/get-to/discussion/<int:id1>")
def get_to_discussion(id1):
    disc = readdb.get_discussion_by_id(id1)
    areaa = readdb.get_area_by_name(disc.area)
    return redirect("/area/"+str(areaa.id)+"/discussion/"+str(id1))

@app.route("/friendlist/dm/search")
def dm_search():
    try:
        is_admin = readdb.is_admin(session["username"])
    except:
        is_admin = False
    areas = readdb.get_areas()
    messages = readdb.get_directmessage_by_search(session["username"], request.args["friend1"], request.args["query"])
    return render_template("directmessagesearch.html", query=request.args["query"], friend=request.args["friend1"], messages=messages, areas=areas, is_admin=is_admin)


#Etusivu, keskustelut, viestit
#frontpage, discussion, messages


@app.route("/")
def index(error=False, error_msg=""):
    try:
        is_admin = readdb.is_admin(session["username"])
    except:
        is_admin = False
    areas = readdb.get_areas()
    return render_template("index.html", areas=areas, is_admin=is_admin, error=error, error_msg=error_msg)

@app.route("/area/<int:id1>")
def area(id1):
    try:
        is_admin = readdb.is_admin(session["username"])
    except:
        is_admin = False
    areas = readdb.get_areas()
    areaa = readdb.get_area_by_id(id1)
    disc = readdb.get_discussions_by_area(areaa.names)
    disc.reverse()
    return render_template("area.html", area=areaa, area_discussions=disc, is_admin=is_admin, ids=[id1], areas=areas)

@app.route("/area/<int:id1>/discussion/<int:id2>")
def discussion(id1, id2, error=False, error_msg=""):
    try:
        is_admin = readdb.is_admin(session["username"])
    except:
        is_admin = False
    areas = readdb.get_areas()
    discussion = readdb.get_discussion_by_id(id2)
    messages = readdb.get_messages_from_discussion(discussion.names)
    return render_template("discussion.html", current_discussion=discussion, ids=[id1,id2],
                            messages=messages, error=error, error_msg=error_msg, is_admin=is_admin, areas=areas)


#Alueiden, keskusteluiden ja viestien luonti
#Creation of areas, discussions and messages


@app.route("/newarea")
def new_area(error=False, error_msg=""):
    try:
        is_admin = readdb.is_admin(session["username"])
    except:
        is_admin = False
    areas = readdb.get_areas()
    return render_template("newarea.html", error=error, error_msg=error_msg, areas=areas, is_admin=is_admin)

@app.route("/newarea/confirm", methods=["POST"])
def new_area_confirm():
    is_admin = readdb.is_admin(session["username"])
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if is_admin:
        writedb.add_area(request.form["title"])
        return redirect("/")
    abort(403)

@app.route("/area/<int:id1>/newdiscussion")
def new_discussion(id1, error=False, error_msg=""):
    try:
        is_admin = readdb.is_admin(session["username"])
    except:
        is_admin = False
    areas = readdb.get_areas()
    return render_template("newdiscussion.html",area=id1, error=error, error_msg=error_msg, areas=areas, is_admin=is_admin)

@app.route("/area/<int:id1>/creatediscussion", methods=["POST"])
def create_discussion(id1):
    print("great")
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    title = request.form["title"]
    message = request.form["body"]
    if not title or not message:
        return new_discussion(id1=id1, error=True, error_msg="Otsikko tai viestikenttä tyhjä")
    area_name = readdb.get_area_by_id(id1).names
    writedb.add_discussion(title, area_name, session["username"])
    writedb.add_message(session["username"], message, title)
    return redirect("/area/"+str(id1))

@app.route("/area/<int:id1>/discussion/<int:id2>/newmessage", methods=["POST"])
def new_message(id1, id2):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    message = request.form["bodyfield"]
    if message is None:
        return discussion(id1=id1, id2=id2, error=True, error_msg="Viestikenttä on tyhjä")
    discussion_name = readdb.get_discussion_by_id(id2).names
    writedb.add_message(session["username"], message, discussion_name)
    return redirect("/area/"+str(id1)+"/discussion/"+str(id2))


#Alueiden, keskusteluiden ja viestien poisto
#deleting areas, discussion and messages


@app.route("/area/<int:id1>/delete", methods=["POST"])
def area_delete(id1):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if not readdb.is_admin(session["username"]):
        abort(403)
    writedb.delete_area(id1)
    return redirect("/")

@app.route("/area/<int:id1>/discussion/<int:id2>/delete", methods=["POST"])
def discussion_delete(id1, id2):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if readdb.get_discussion_by_id(id2).starter == session["username"] or readdb.is_admin(session["username"]):
        writedb.delete_discussion(id2)
        return redirect("/area/"+str(id1))
    abort(403)

@app.route("/area/<int:id1>/discussion/<int:id2>/msg-delete/<int:id3>", methods=["POST"])
def msg_delete(id1, id2, id3):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if readdb.get_message_by_id(id3).writer == session["username"] or readdb.is_admin(session["username"]):
        writedb.delete_message(id3)
        return redirect("/area/"+str(id1)+"/discussion/"+str(id2))
    abort(403)
