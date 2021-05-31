from app import app, db
from models import User, Todo
from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/')
@login_required
def index():
    # GET REQUEST
    user_todos = current_user.todo
    return render_template("main.html", user_todos=user_todos)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_register'))

@app.route('/register')
@app.route('/login')
def login_register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    route_info = request.url_rule
    if 'login' in route_info.rule:
        return render_template("login.html")

    return render_template("register.html")

@app.route('/login-api', methods=["GET", "POST"])
def login_api():
    if request.method == "POST":
        login_req = request.get_json(force=True)
        username = login_req.get('username', None)
        password = login_req.get('password', None)
        
        user = db.session.query(User).filter(User.username == username).first()
        if user is None:
            return {"message": "Username or password is incorrect."}, 200
        
        if not user.check_password(password):
            return {"message": "Username or password is incorrect."}, 200
           
        login_user(user, remember=True)
        return {"message": "OK"}, 200

# INSERT METHOD
@app.route('/register-api', methods=["GET", "POST"])
def register_api():
    if request.method == "POST":
        register_req = request.get_json(force=True)
        username =     register_req.get('username', None)
        password =     register_req.get('password', None)
        
        user = db.session.query(User).filter(User.username == username).first()
        if user is not None:
            return {"message": "User with this username is already exists."}, 200
        
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user, remember=True)
        return {"message": "OK"}, 200

# DELETE METHOD
@app.route("/delete-todo", methods=["GET", "POST"])
@login_required
def delete_todo():
    if request.method == "POST":
        delete_req = request.get_json(force=True)
        todo_id = delete_req.get("todo_id", None)
        
        todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
        if todo is None:
            return {"message": "Todo element is not exist or already deleted."}, 200
        
        db.session.delete(todo)
        db.session.commit()
        
        return {"message": "OK"}, 200
    
# UPDATE METHOD
@app.route("/change-todo-complete", methods=["GET", "POST"])
def change_todo_complete():
    if request.method == "POST":
        change_req = request.get_json(force=True)
        todo_id = change_req.get("todo_id", None)
        new_c_v = change_req.get("new_c_v", None)
        
        todo = Todo.query.filter_by(id = todo_id).first()
        todo.complete_bool = new_c_v
        db.session.commit()
        
        return {"message": "OK"}, 200

@app.route("/add-todo", methods=["GET", "POST"])
def add_todo():
    if request.method == "POST":
        req = request.get_json(force=True)
        name = req.get("name", None)
        
        todo = Todo(name=name, complete_bool=False, owner=current_user)
        db.session.add(todo)
        db.session.commit()
        
        return {"message": "OK", "todo_id": todo.id}
