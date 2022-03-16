const deleteBtns = document.querySelectorAll(".dropdown-item");
[...deleteBtns].map((btn) =>
  btn.addEventListener("click", (event) => deleteLike(event))
);

function deleteLike(event) {
  event.preventDefault();
  let { target } = event;
  while (target.tagName !== "TR") {
    target = target.parentNode;
  }
  const track_id = target.dataset.track_id;
  const weather = target.dataset.weather;
  fetch("/api/delete-like", {
    method: "DELETE",
    headers: {
      "Content-type": "application/json",
    },
    body: JSON.stringify({
      track_id,
      weather,
    }),
  })
    .then((res) => res.json())
    .then((json) => console.log(json));
  window.location.reload();
}
