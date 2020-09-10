btn.addEventListener("click", btnClick);
                function btnClick() {
                    let login = document.getElementById("UserLogin").value;
                    let password = document.getElementById("UserPassword").value;
                    let mail = document.getElementById("UserMail").value;
                    let FIO = document.getElementById("UserName").value;
                    user = {
                        UserLogin: login,
                        UserPassword: password,
                        UserMail: mail,
                        UserName: FIO
                    }
                    url ="http://iamalinin.variag.local:5050/send"
                    fetch(url ,{
                    method: "POST",
                    headers:{"content-type":"application/json; charset=utf-8"}, 
                    body: JSON.stringify(user)
                }).then(response => response.json())
                .then(commits => alert(commits))
                }