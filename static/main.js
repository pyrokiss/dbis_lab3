
function delete_todo(todo_id) {

    fetch('/delete-todo', {
        method: 'post',
        body: JSON.stringify({"todo_id": todo_id})
      }).then(r => r.json())
        .then(res => {
          if (res.message === "OK") {
            var el = document.getElementById('todo_' + todo_id + "_");
            el.remove();
          } else {
            alert(res.message);
          }
        })
}

function change_todo_complete(todo_id) {
    var new_checkbox_value = document.getElementById('check' + todo_id).checked;

    creds = {
        "todo_id": todo_id,
        "new_c_v": new_checkbox_value
    }

    fetch('/change-todo-complete', {
        method: 'post',
        body: JSON.stringify(creds),
      }).then(r => r.json())
        .then(res => {
            console.log(res.message);
        })
}

function add_data() {
    var name = document.getElementById("add_data_input").value;

    if (!name.trim()) {
      alert("Input todo name.");
      return
    }

    fetch('/add-todo', {
        method: 'post',
        body: JSON.stringify({"name": name}),
      }).then(r => r.json())
        .then(res => {
            console.log(res);
            var li = document.createElement("li");
            li.setAttribute("id", "todo_" + res.todo_id + "_");
            li.setAttribute("class", "list-group-item d-flex");
            li.setAttribute("style", "justify-content: space-between;");
            li.innerHTML = 
                    `<div class="custom-control custom-checkbox">\
                       <input type="checkbox" class="custom-control-input" id=${"check" + res.todo_id} onclick=${"change_todo_complete(" + res.todo_id + ")"}>
                        <label class="custom-control-label" for=${"check" + res.todo_id} style="font-size: 3">${name}</label>\
                    </div> <div class="custom-control">\
                        <button class="btn btn-danger" onclick=${ "delete_todo(" + res.todo_id + ")"}>Delete</button> </div>`;
            document.getElementById("todo-list-ul").appendChild(li);

            var name_element = document.getElementById("add_data_input");
            name_element.value = "";
        })
}
