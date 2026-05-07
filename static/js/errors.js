function displayError(msg, element) {
  const span = document.createElement("span");
  span.textContent = msg;
  span.className = "error visible";
  element.appendChild(span);
}

function displayErrorHead(msg, element) {
  const span = document.createElement("span");
  const txt = document.createElement("h2");
  txt.textContent = msg;
  span.className = "error-head visible";
  span.appendChild(txt);
  element.prepend(span);
}

function displayErrors(head, msgs, element){
  displayErrorHead(head, element);
  for (let i = 0; i < msgs.length; i++) {
    displayError(msgs[i], element)
  }
  const hline = document.createElement("hr")
  element.appendChild(hline)
}


function cleanErrors(element) {
  element.innerHTML = "";
}