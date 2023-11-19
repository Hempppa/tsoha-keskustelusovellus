from flask import redirect, render_template, request, session, abort
import readdb
import writedb
from app import app


#Käyttäjä keskeiset sivut
#User centric pages


@app.route("/account")
def account(error=False, error_msg=""):
    return render_template("account.html", error=error, error_msg=error_msg)

@app.route("/newaccount")
def newaccount(error=False, error_msg=""):
    return render_template("newaccount.html", error=error, error_msg=error_msg)

@app.route("/create", methods=["POST"])
def create():
    name = request.form["accname"]
    password = request.form["passwrd"]
    if password == None or name == None or name == "" or password == "":
        return newaccount(True, "Nimi tai salasanakenttä tyhjä")
    #Tähän sitten salasanan laatutarkastus
    #elif (len(password) < 8) or (name in password):
        #return "<script>alert('Kelvoton salasana')</script><script>document.location='/newaccount'</script>"
    if writedb.add_user(name, password):
        session["username"] = name
        return redirect("/")
    return newaccount(True, "Käyttäjänimi varattu")

@app.route("/login", methods=["POST"])
def login():
    name = request.form["accname"]
    password = request.form["passwrd"]    
    if readdb.confirm_user_pass(name, password):
        session["username"] = name
        return redirect("/")
    return account(True, "Väärä nimi tai salasana")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/personal")
def personal(msg=False, msg_content=""):
    return render_template("personal.html", msg=msg, msg_content=msg_content)

@app.route("/started")
def started():
    discussions = readdb.get_discussion_by_writer(session["username"])
    return render_template("personaldiscussions.html", discussions=discussions)

@app.route("/friendlist")
def friends(request=False, req_msg=""):
    friendlist = readdb.get_friends_by_user(session["username"])
    return render_template("friendlist.html", friends=friendlist, request=request, req_msg=req_msg)

@app.route("/friendlist/send")
def friendsend(request=False, req_msg=""):
    return render_template("friendsend.html", request=request, req_msg=req_msg)

@app.route("/friendlist/send/confirm", methods=["POST"])
def sendfriend():
    if readdb.check_user_exist(request.form["friend"]):
        writedb.add_friend(session["username"], request.form["friend"])
        return friends(True, "Kaverikutsu lähetetty")
    return friendsend(True, "Käyttäjää ei löydy")

@app.route("/friendlist/received")
def sentrequests():
    requested = readdb.get_friend_requests(session["username"])
    return render_template("requests.html", requested=requested)

@app.route("/changepass")
def changepass(error=False, error_msg=""):
    return render_template("changepass.html", error=error, error_msg=error_msg)

@app.route("/changepass/confirm", methods=["POST"])
def changeconfirm():
    if readdb.confirm_user_pass(session["username"], request.form["oldpasswrd"]) and not (request.form["newpasswrd"] == None or request.form["newpasswrd"] == ""):
        writedb.change_user_pass(session["username"], request.form["newpasswrd"])
        return redirect("/personal")
    else:
        return changepass(True, "väärä salasana")

@app.route("/rmvuser")
def rmvuser():
    return render_template("rmvuser.html")

@app.route("/rmvuser/confirm", methods=["POST"])
def rmvconfirm():
    if readdb.confirm_user_pass(request.form["accname"], request.form["passwrd"]):
        writedb.delete_user(request.form["accname"])
        del session["username"]
        return redirect("/")


#hakutoiminnot
#search functionality


@app.route("/search")
def search():
    discussions = readdb.get_discussion_by_search(request.args["query"], None)
    return render_template("search.html", query=request.args["query"], discussions=discussions, id1=None)

@app.route("/area/<int:id>/search")
def areasearch(id):
    discussions = readdb.get_discussion_by_search(request.args["query"], id)
    print(discussions)
    return render_template("search.html", query=request.args["query"], discussions=discussions, id1=id)

@app.route("/area/<int:id1>/discussion/<int:id2>/search")
def discussionsearch(id1, id2):
    messages = readdb.get_message_by_search(request.args["query"], id2)
    return render_template("messagesearch.html", query=request.args["query"], messages=messages, ids=[id1, id2])

@app.route("/get-to/discussion/<int:id>")
def getToDiscussion(id):
    discussion = readdb.get_discussion_by_id(id)
    area = readdb.get_area_by_name(discussion.area)
    return redirect("/area/"+str(area.id)+"/discussion/"+str(id))


#Etusivu, keskustelut, viestit
#frontpage, discussion, messages


@app.route("/")
def index():
    is_admin = False
    try:
        if session["username"]:
            is_admin = readdb.is_admin(session["username"])
    except:
        pass
    areas = readdb.get_areas()
    return render_template("index.html", areas=areas, is_admin=is_admin)

@app.route("/area/<int:id>")
def area(id):
    area = readdb.get_area_by_id(id)
    discussions = readdb.get_discussions_by_area(area.names)
    discussions.reverse()
    return render_template("area.html", area=area, area_discussions=discussions)

@app.route("/area/<int:id1>/discussion/<int:id2>")
def discussion(id1, id2, error=False, error_msg=""):
    discussion = readdb.get_discussion_by_id(id2)
    messages = readdb.get_messages_from_discussion(discussion.names)
    return render_template("discussion.html", current_discussion=discussion, ids=[id1,id2], messages=messages, error=error, error_msg=error_msg)


#Alueiden, keskusteluiden ja viestien luonti
#Creation of areas, discussions and messages


@app.route("/newarea")
def newarea(error=False, error_msg=""):
    is_admin = False
    if session["username"] != None:
        is_admin = readdb.is_admin(session["username"])
    if is_admin:
        return render_template("newarea.html", error=error, error_msg=error_msg)
    else:
        abort(403)

@app.route("/newarea/confirm", methods=["POST"])
def newareaconfirm():
    is_admin = False
    if session["username"] != None:
        is_admin = readdb.is_admin(session["username"])
    if is_admin:
        writedb.add_area(request.form["title"])
        return redirect("/")
    else:
        abort(403)

@app.route("/area/<int:id>/newdiscussion")
def newdiscussion(id, error=False, error_msg=""):
    return render_template("newdiscussion.html",area=id, error=error, error_msg=error_msg)

@app.route("/area/<int:id>/creatediscussion", methods=["POST"])
def creatediscussion(id):
    title = request.form["title"]
    message = request.form["body"]
    if title == None or message == None or title == "" or message == "":
        return newdiscussion(id=id, error=True, error_msg="Otsikko tai viestikenttä tyhjä")
    area_name = readdb.get_area_by_id(id).names
    writedb.add_discussion(title, area_name, session["username"])
    writedb.add_message(session["username"], message, title)
    return redirect("/area/"+str(id))

@app.route("/area/<int:id1>/discussion/<int:id2>/newmessage", methods=["POST"])
def newmessage(id1, id2):
    message = request.form["bodyfield"]
    if message == None:
        return discussion(id1=id1, id2=id2, error=True, error_msg="Viestikenttä on tyhjä")
    discussion_name = readdb.get_discussion_by_id(id2).names
    writedb.add_message(session["username"], message, discussion_name)
    return redirect("/area/"+str(id1)+"/discussion/"+str(id2))


#Alueiden, keskusteluiden ja viestien poisto


@app.route("/area/<int:id1>/discussion/<int:id2>/msg-delete/<int:id3>", methods=["POST"])
def msgDelete(id1, id2, id3):
    if readdb.get_message_by_id(id3).writer == session["username"]:
        writedb.delete_message(id3)
    else:
        abort(403)