const loginForm = document.querySelector(".login-form > form");
const joinForm = document.querySelector("#join");

function postLogin(event) {
  event.preventDefault();
  const { target } = event;
  const username = target.querySelector("#signin_id").value;
  const password = target.querySelector("#signin_pass").value;
  try {
    fetch("/login", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
      }),
    })
      .then((res) => res.json())
      .then((json) => {
        const { msg, redirect_url } = json;
        if (msg === "성공!") {
          window.location.href = redirect_url;
        } else {
          alert(msg);
          window.location.href = redirect_url;
        }
      });
  } catch (e) {
    console.log(e);
  }
}

function postJoin(event) {
  event.preventDefault();
  const { target } = event;
  const username = target.querySelector("#signup_id").value;
  const password = target.querySelector("#sign_pass").value;
  const password2 = target.querySelector("#sign_pass2").value;
  try {
    fetch("/join", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
        password2,
      }),
    })
      .then((res) => res.json())
      .then((json) => {
        const { ok, err } = json;
        if (ok === true) {
          alert("회원가입 되었습니다. 로그인 해 주세요.");
        } else {
          alert(err);
        }
        window.location.href = "/login";
      });
  } catch (e) {
    console.log(e);
  }
}

loginForm.addEventListener("submit", (event) => postLogin(event));
joinForm.addEventListener("submit", (event) => postJoin(event));
