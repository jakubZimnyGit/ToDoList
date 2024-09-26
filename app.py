from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

todos = [{'task': 'connect with postgreSQL :D', 'done': False}]

@app.route("/")
def index():
    return render_template('index.html', todos=todos)

def updateTodos():
    done_todos=request.form.getlist('done')
    if not done_todos:
        for todo in todos:
            todo['done'] = False
    for todo in todos:
        for index in done_todos:
            if todo == todos[int(index)]:
                todo['done'] = True
                break
            else:
                todo['done'] = False


@app.route("/submit", methods=["POST"])
def submit():
    print(request.form['btn'])
    if request.form['btn'] == 'check':
        
        check()

    elif request.form['btn'] == 'delete':
        deleteAllChecked()
    
    return redirect(url_for("index"))

def deleteAllChecked():
    updateTodos()
    global todos
    todos = [todo for todo in todos if not todo['done']]
    return redirect(url_for("index"))

def check():
    updateTodos()
    #return todos  #PORRÓWNAC LISTE TODOS Z OTRZYMANYM WYNIKIEM ABY WIEDZIEC KTORE ZOSTALY ODZNACZONE ESSA
    return redirect(url_for("index"))


@app.route("/add", methods = ["POST"])
def add():
    todo=request.form['todo']
    todos.append({'task': todo, 'done': False})
    return redirect(url_for("index"))


@app.route("/edit/<int:index>", methods = ['GET', 'POST'])
def edit(index):
    todo=todos[index]
    if request.method == "POST":
        todo["task"] = request.form["todo"]
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", todo=todo, index=index)


@app.route("/delete/<int:index>")
def delete(index):
    del todos[index]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=int(3000), host="0.0.0.0")