
function submit_register() {
    var username = document.getElementById('register-username').value;
    var password = document.getElementById('register-password').value;
    var password_confirm = document.getElementById('register-password-confirm').value;

    if (!username.trim() || !password.trim() || !password_confirm.trim()) {
        alert("Blank username or passwords.");
        return
    }

    if (password !== password_confirm) {
        alert("Passwords must be the same.");
        return
    }

    creds = {
        "username": username,
        "password": password
    };

    // fetch data from server
    fetch('/register-api', {
        method: 'post',
        body: JSON.stringify(creds),
        redirect: 'follow'
      }).then(r => r.json())
        .then(res => {
          if (res.message === "OK") {
              window.location.href = "/";
          } else {
            alert(res.message);
          }
        })
}
