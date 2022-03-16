const loginForm = document.querySelector(".login-form > form");
const joinForm = document.querySelector("#join");

async function postLogin(event) {
  event.preventDefault();
  const { target } = event;
  const username = target.querySelector("#signin_id").value;
  const password = target.querySelector("#signin_pass").value;
  try {
    const response = await fetch("/login", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
      }),
    });
    if (response.code !== 200) {
      window.location.reload();
    } else {
      window.location.href("/");
    }
    console.log(response);
  } catch (e) {
    console.log(e);
  }
}

async function postJoin(event) {
  event.preventDefault();
  const { target } = event;
  const username = target.querySelector("#signup_id").value;
  const password = target.querySelector("#sign_pass").value;
  const password2 = target.querySelector("#sign_pass2").value;
  try {
    const response = await fetch("/join", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
        password2,
      }),
    });
    if (response.code !== 200) {
      window.location.reload();
    } else {
      window.location.href("/");
    }
    console.log(response);
  } catch (e) {
    console.log(e);
  }
}

loginForm.addEventListener("submit", (event) => postLogin(event));
joinForm.addEventListener("submit", (event) => postJoin(event));
