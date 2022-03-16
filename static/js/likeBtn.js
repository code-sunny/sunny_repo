const weatherLikeBtns = document.querySelectorAll(".weather-likeBtn");
[...weatherLikeBtns].map(btn => btn.addEventListener("click", (e) => likeBtn(e)));
function likeBtn(event) {
    event.preventDefault();
    let {target} = event;
    if (target.tagName === "IMG") {
    target = target.parentNode;
    }
    let targetContainer = document.querySelector(".modal-content");
    const weatherValue = target.value;
    const track_id = targetContainer.dataset.track_id;
    let liked = "False";
    if ([...target.classList].some(x => x === "liked")) {
        liked = "True";
    }
    fetch("/api/like-btn", {
        method:"POST",
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify({
            track_id: track_id,
            weather: weatherValue,
            weather_like_state: liked,
        })
    }).then(res => res.json()).then(json => console.log(json));
    target.classList.toggle("liked");
}