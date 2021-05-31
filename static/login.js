
function submit_login() {
    var username = document.getElementById('login-username').value;
    var password = document.getElementById('login-password').value;

    if (!username.trim() || !password.trim()) {
        alert("Blank username or password.");
        return
    }

    creds = {
        "username": username,
        "password": password
    };

    // fetch data from server
    fetch('/login-api', {
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
