async function sendMessage() {
    const input = document.getElementById("input");
    const message = input.value.trim();

    if (!message) return;

    const chatBox = document.getElementById("chat-box");

    // session id
    let session_id = localStorage.getItem("session_id");
    if (!session_id) {
        session_id = "user_" + Math.random().toString(36).substr(2, 9);
        localStorage.setItem("session_id", session_id);
    }

    chatBox.innerHTML += `<p class="user">You: ${message}</p>`;

    try {
        const res = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",   // ✅ REQUIRED
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({   // ✅ REQUIRED
                message: message,
                session_id: session_id
            })
        });

        if (!res.ok) {
            throw new Error("Server response not OK");
        }

        const data = await res.json();

        chatBox.innerHTML += `<p class="bot">Bot: ${data.reply}</p>`;

    } catch (error) {
        console.error("ERROR:", error);
        chatBox.innerHTML += `<p class="bot">⚠️ Server error</p>`;
    }

    input.value = "";
}