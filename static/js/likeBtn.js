const weatherLikeBtns = document.querySelectorAll(".weather-likeBtn");
[...weatherLikeBtns].map((btn) =>
  btn.addEventListener("click", (e) => likeBtn(e))
);
function likeBtn(event) {
  event.preventDefault();
  let { target } = event;
  if (target.tagName === "IMG") {
    target = target.parentNode;
  }
  let targetContainer = target.parentNode;
  console.log(targetContainer.className);
  if (targetContainer.className === "weather_icon") {
    while (targetContainer.className !== "modal-content") {
      targetContainer = targetContainer.parentNode;
    }
  } else {
    while (targetContainer.className !== "chart_column") {
      targetContainer = targetContainer.parentNode;
    }
  }
  const weatherValue = target.value;
  const track_id = targetContainer.dataset.track_id;
  fetch("/api/like-btn", {
    method: "POST",
    headers: {
      "Content-type": "application/json",
    },
    body: JSON.stringify({
      track_id: track_id,
      weather: weatherValue,
    }),
  })
    .then((res) => res.json())
    .then((json) => {
      console.log(json);
      if (json["msg"] == "먼저 로그인 해주세요!") {
        alert(json["msg"]);
        let redirect_url = json["redirect_url"];
        window.location.href = redirect_url;
      }
    });
}
