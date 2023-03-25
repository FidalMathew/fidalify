let query = { active: true, currentWindow: true };

chrome.tabs.query(query, gotTabs);

function gotTabs(tabs) {
  let msg = {
    txt: "hello from popup",
  };

  chrome.tabs.sendMessage(tabs[0].id, msg, function (response) {
    if (!response) {
      document.getElementById("phonetic").innerHTML = "Welcome!";
      document.getElementById("example").innerHTML =
        "Please select a word to find its definition.";
    } else if (response.swor === "_TextNotSelected_") {
      document.getElementById("error").innerHTML = "Please select a word!";
    } else {
      let swo = response.swor;
      swo = swo.replace(/[^a-zA-Z ]/g, " ");
      dictionary(swo);
    }
  });
}

async function dictionary(query) {

  console.log("Dictionary", query)

  try {
    let res = await fetch("http://localhost:5000/", {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ "query": query })
    })
    res = await res.text()

    console.log(typeof (res))
    res = JSON.parse(res)
    console.log(res)
    let newsHeading = document.getElementById("newsHeading")
    newsHeading.innerHTML = res.ans

    // checking res.authenticity

    let error = document.getElementById("error")
    let correct = document.getElementById("correct")

    if (res.authenticity === 1) {
      correct.style.display = "block"
      error.style.display = "none"
    }
    else if (res.authenticity === 0) {
      error.style.display = "block"
      correct.style.display = "none"
    }

  } catch (error) {
    console.log(error)
  }


}
