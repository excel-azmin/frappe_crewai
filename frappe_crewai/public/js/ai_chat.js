document.addEventListener("DOMContentLoaded", function () {
    const chatButton = document.createElement('div');
    chatButton.id = 'ai-chat-button';
    chatButton.innerHTML = '💬';
    document.body.appendChild(chatButton);

    const chatWindow = document.createElement('div');
    chatWindow.id = 'ai-chat-window';
    chatWindow.innerHTML = `
        <div id="ai-chat-header">AI Assistant <span id="ai-chat-close">×</span></div>
        <div id="ai-chat-body"></div>
        <input type="text" id="ai-chat-input" placeholder="Ask me anything..." />
    `;
    document.body.appendChild(chatWindow);

    chatButton.onclick = () => {
        chatWindow.style.display = 'block';
        chatButton.style.display = 'none';
    };

    document.getElementById('ai-chat-close').onclick = () => {
        chatWindow.style.display = 'none';
        chatButton.style.display = 'block';
    };

    document.getElementById('ai-chat-input').addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            const query = this.value;
            if (!query) return;

            const chatBody = document.getElementById('ai-chat-body');
            chatBody.innerHTML += `<div class="user-msg">${query}</div>`;
            this.value = '';

            frappe.call({
                method: 'frappe_crewai.api.ai_query.ask_ai',
                args: { query },
                callback: function (r) {
                    if (r.message?.result) {
                        chatBody.innerHTML += `<div class="ai-msg">${r.message.result}</div>`;
                        chatBody.scrollTop = chatBody.scrollHeight;
                    } else {
                        chatBody.innerHTML += `<div class="ai-msg error">Error fetching response</div>`;
                    }
                }
            });
        }
    });
});
