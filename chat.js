const ws = new WebSocket('ws://localhost:5000');

ws.onmessage = (event) => {
    const chat = document.getElementById('chat');
    const message = document.createElement('div');
    message.textContent = event.data;
    message.classList.add('other-message');
    chat.appendChild(message);
    chat.scrollTop = chat.scrollHeight;
};

function sendMessage() {
    const input = document.getElementById('message');
    const chat = document.getElementById('chat');
    const message = document.createElement('div');
    message.textContent = `You: ${input.value}`;
    message.classList.add('user-message');
    chat.appendChild(message);
    chat.scrollTop = chat.scrollHeight;
    ws.send(input.value);
    input.value = '';
}
