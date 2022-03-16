$(document).ready(function () {
  console.log("성공");
  song_info();
});

async function showRank(event) {
  const {
    target: { value },
  } = event;
  try {
    const response = await fetch(`/main/song-rank?moveBtn=${value}`);
    console.log(await response.json());
  } catch (e) {
    console.log(e);
  }
}

async function songLike(event) {
  const { target } = event;
  const likeCountSpan = target.nextSibling.nextSibling;
  const { value: weather } = target;
  let is_liked = Boolean(target.dataset.liked);
  const track_id = document.querySelector("#music-box").dataset.track_id;
  try {
    const { likes } = await (
      await fetch("/api/like-btn", {
        method: "POST",
        headers: {
          "Content-type": "application/json",
        },
        body: JSON.stringify({
          track_id,
          weather,
          is_liked,
        }),
      })
    ).json();
    is_liked = is_liked ? "True" : "False";
    target.dataset.liked = is_liked;
    likeCountSpan.innerText = likes;
  } catch (e) {
    console.log(e);
  }
}

function song_info() {
  $.ajax({
    type: "GET",
    url: "/api/song-info",
    data: {},
    success: function (response) {
      console.log(response["song_list"]);
    },
  });
}

const moveBtns = document.querySelectorAll(".moveBtn");
[...moveBtns].map((btn) =>
  btn.addEventListener("click", (event) => showRank(event))
);

const weatherLikeBtns = document.querySelectorAll(".weather-like-btn");
[...weatherLikeBtns].map((btn) =>
  btn.addEventListener("click", (event) => songLike(event))
);
