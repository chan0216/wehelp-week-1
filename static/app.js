function uploadFile(event) {
  event.preventDefault();
  let text = document.querySelector("#text").value;
  let file = document.querySelector("#file").files[0];
  let data = new FormData();
  data.append("file", file);
  data.append("text", text);
  fetch("/upload", {
    method: "POST",
    body: data,
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      let hr = document.createElement("hr");
      let img = document.createElement("img");
      let text = document.createElement("p");
      text.textContent = data["text"];
      img.src = data["imgurl"];
      document.body.append(hr, text, img);
    });
}

fetch("/getdata")
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    let res = data["data"];
    for (const obj of res) {
      let hr = document.createElement("hr");
      let img = document.createElement("img");
      let text = document.createElement("p");
      text.textContent = obj["text"];
      img.src = obj["imgurl"];
      document.body.append(hr, text, img);
    }
  });
