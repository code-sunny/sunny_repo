const get_recommend = document.getElementById("get-recommend");
get_recommend.addEventListener("click", () => getWeather());
let weatherInfo;
function getWeather() {
  if (!navigator.geolocation) {
    let response = fetch("/get-weather", {
      method: "POST",
    }).then((res) => res.json());
    console.log("not", response);
  } else {
    navigator.geolocation.getCurrentPosition(
      // success
      (position) => {
        let response = fetch("/get-weather", {
          method: "POST",
          headers: {
            "Content-type": "application/json",
          },
          body: JSON.stringify({
            lat: position.coords.latitude,
            lon: position.coords.longitude,
          }),
        })
          .then((res) => res.json())
          .then((json) => console.log(json));

        console.log(response);
      },
      // error
      (error) => {
        // console.log(error);
        fetch("/get-weather", {
          method: "POST",
        })
          .then((res) => res.json())
          .then((json) => (weatherInfo = json))
          .then(() => {
            let { weather, temp } = weatherInfo;
            document.getElementById("now_temperature").innerText = temp;
          });
      }
    );
  }
}
// getWeather();
