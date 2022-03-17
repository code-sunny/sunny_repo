const loginForm = document.querySelector(".login-form > form");
const joinForm = document.querySelector("#join");

function postLogin(event) {
  event.preventDefault();
  const { target } = event;
  const username = target.querySelector("#signin_id").value;
  const password = target.querySelector("#signin_pass").value;
  try {
    if (username === undefined) {
      alert("아이디를 입력해주세요.");
      throw Error;
    } else if (username.length < 3) {
      alert("3자 이상의 아이디를 입력해주세요.");
      throw Error;
    } else if (password === undefined) {
      alert("비밀번호를 입력해주세요.");
      throw Error;
    } else if (password.length < 4) {
      alert("비밀번호의 길이가 짧습니다.");
      throw Error;
    }
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
    if (username.length < 3) {
      alert("4자 이상의 username을 입력해주세요");
      throw Error;
    } else if (password.length < 4) {
      alert("5자 이상의 비밀번호를 사용해주세요");
      throw Error;
    } else if (password !== password2) {
      alert("비밀번호가 일치하지 않습니다.");
      throw Error;
    }
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
