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
  let targetContainer = document.querySelector(".song-content");
  const weatherValue = target.value;
  const track_id = targetContainer.dataset.track_id;
  let liked = "False";
  if ([...target.classList].some((x) => x === "liked")) {
    liked = "True";
  }
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
        window.location.replace(redirect_url);
      }
    });
  target.classList.toggle("liked");
}
