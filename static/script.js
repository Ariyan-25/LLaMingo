document.getElementById("chat-form").addEventListener("submit", async function (e) {
  e.preventDefault();
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  const chatBox = document.getElementById("chat-box");
  chatBox.innerHTML += `<div class="chat-bubble user">${message}</div>`;
  input.value = "";

  const typing = document.getElementById("typing-indicator");
  typing.style.display = "block";

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message })
    });

    const data = await res.json();
    chatBox.innerHTML += `<div class="chat-bubble bot">${data.response}</div>`;
  } catch (err) {
    chatBox.innerHTML += `<div class="chat-bubble bot">Error: Could not reach server.</div>`;
  } finally {
    typing.style.display = "none";
  }

  chatBox.scrollTop = chatBox.scrollHeight;
});
