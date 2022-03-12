// import { getWeather } from "./setWeather";
let weatherInfo;

function getWeather() {
  let weatherInfo = [];
  if (!navigator.geolocation) {
    fetch("/get-weather", {
      method: "POST",
    });
  } else {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        fetch("/get-weather", {
          method: "POST",
          body: JSON.stringify({
            lat: position.coords.latitude,
            lon: position.coords.longitude,
          }),
          headers: {
            "Content-type": "application/json",
          },
        })
          .then((response) => response.json())
          .then((json) => {
            weatherInfo = json.weather[0];
            console.log(weatherInfo);
          });
      },
      (error) => {
        console.log(error);
      }
    );
  }
  return weatherInfo;
}

function App() {
  console.log("Hello world!");
  weatherInfo = getWeather();
}

App();
