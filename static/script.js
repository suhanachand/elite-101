const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");

function addMessage(sender, text) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);
  msg.innerHTML = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;
  addMessage("user", text);
  userInput.value = "";

  const response = await fetch("/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message: text})
  });

  const data = await response.json();
  addMessage("bot", data.reply);
}

// Start chat automatically
window.onload = () => {
  fetch("/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message: ""})
  })
  .then(res => res.json())
  .then(data => addMessage("bot", data.reply));
};
