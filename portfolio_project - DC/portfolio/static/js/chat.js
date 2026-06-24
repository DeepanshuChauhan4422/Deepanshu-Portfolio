/* =========================================================================
   DEEPANSHU CHAUHAN PORTFOLIO - AI CHAT ASSISTANT SCRIPTS
   Handles: Chat UI, History, Typing Effect, API Calls, Markdown Formatting
   ========================================================================= */

document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const quickQBtns = document.querySelectorAll('.quick-q-btn');
    
    let chatHistory = [];

    // --- 1. Helper: Format Date/Time ---
    function getFormattedTime() {
        const now = new Date();
        let hours = now.getHours();
        let minutes = now.getMinutes();
        const ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12; // 0 should be 12
        minutes = minutes < 10 ? '0' + minutes : minutes;
        return `${hours}:${minutes} ${ampm}`;
    }

    // --- 2. Helper: Clean HTML/Markdown parsing ---
    function formatMessageText(text) {
        const lines = text.split('\n');
        let formattedHtml = '';
        let inList = false;
        
        for (let i = 0; i < lines.length; i++) {
            let line = lines[i];
            let trimmed = line.trim();
            
            // Headers
            if (trimmed.startsWith('### ')) {
                if (inList) { formattedHtml += '</ul>'; inList = false; }
                formattedHtml += `<h3>${trimmed.substring(4)}</h3>`;
                continue;
            }
            if (trimmed.startsWith('## ')) {
                if (inList) { formattedHtml += '</ul>'; inList = false; }
                formattedHtml += `<h2>${trimmed.substring(3)}</h2>`;
                continue;
            }
            if (trimmed.startsWith('# ')) {
                if (inList) { formattedHtml += '</ul>'; inList = false; }
                formattedHtml += `<h1>${trimmed.substring(2)}</h1>`;
                continue;
            }
            
            // List Items
            if (trimmed.startsWith('- ') || trimmed.startsWith('* ') || (trimmed.match(/^\d+\.\s/) && trimmed.length > 3)) {
                let isOrdered = trimmed.match(/^\d+\.\s/);
                let listTag = isOrdered ? 'ol' : 'ul';
                
                if (!inList) {
                    formattedHtml += `<${listTag}>`;
                    inList = listTag;
                } else if (inList !== listTag) {
                    formattedHtml += `</${inList}><${listTag}>`;
                    inList = listTag;
                }
                
                let itemContent = isOrdered ? trimmed.replace(/^\d+\.\s/, '') : trimmed.substring(2);
                itemContent = itemContent.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                itemContent = itemContent.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>');
                formattedHtml += `<li>${itemContent}</li>`;
                continue;
            }
            
            // End of list check
            if (inList && trimmed !== '') {
                formattedHtml += `</${inList}>`;
                inList = false;
            }
            
            if (trimmed === '') {
                if (inList) {
                    formattedHtml += `</${inList}>`;
                    inList = false;
                }
                formattedHtml += '<br/>';
            } else {
                let parsedLine = trimmed.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                parsedLine = parsedLine.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>');
                formattedHtml += `<p>${parsedLine}</p>`;
            }
        }
        
        if (inList) {
            formattedHtml += `</${inList}>`;
        }
        
        return formattedHtml;
    }

    // --- 3. UI: Append Message Bubble ---
    function appendMessage(sender, text, isGreeting = false) {
        if (!chatMessages) return;

        // Remove typing indicator if present
        const typingIndicator = document.getElementById('typing-indicator-bubble');
        if (typingIndicator) {
            typingIndicator.remove();
        }

        const bubble = document.createElement('div');
        bubble.className = `message-bubble ${sender}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = sender === 'ai' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';
        
        const wrapper = document.createElement('div');
        wrapper.className = 'message-content-wrapper';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        content.innerHTML = isGreeting ? text : formatMessageText(text);
        
        const time = document.createElement('span');
        time.className = 'message-time';
        time.innerText = getFormattedTime();
        
        wrapper.appendChild(content);
        wrapper.appendChild(time);
        
        bubble.appendChild(avatar);
        bubble.appendChild(wrapper);
        
        chatMessages.appendChild(bubble);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Save to local history
        if (!isGreeting) {
            chatHistory.push({
                role: sender === 'ai' ? 'assistant' : 'user',
                content: text
            });
        }
    }

    // --- 4. UI: Show Typing Animation ---
    function showTypingIndicator() {
        if (!chatMessages) return;
        
        // Prevent duplicate indicators
        if (document.getElementById('typing-indicator-bubble')) return;

        const bubble = document.createElement('div');
        bubble.id = 'typing-indicator-bubble';
        bubble.className = 'message-bubble ai';
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = '<i class="fas fa-robot"></i>';
        
        const wrapper = document.createElement('div');
        wrapper.className = 'message-content-wrapper';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const typing = document.createElement('div');
        typing.className = 'typing-indicator';
        typing.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        
        content.appendChild(typing);
        wrapper.appendChild(content);
        bubble.appendChild(avatar);
        bubble.appendChild(wrapper);
        
        chatMessages.appendChild(bubble);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // --- 5. Backend: Send Message to API ---
    async function sendMessage(text) {
        // Render user message bubble
        appendMessage('user', text);
        
        // Show AI is typing
        showTypingIndicator();

        try {
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Get Django CSRF token
                },
                body: JSON.stringify({
                    message: text,
                    history: chatHistory
                })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // Append bot reply
            setTimeout(() => {
                appendMessage('ai', data.reply);
            }, 800); // Slight delay for realistic chat feel

        } catch (error) {
            console.error('Error sending chat message:', error);
            setTimeout(() => {
                appendMessage('ai', "I'm sorry, I'm having trouble connecting to my brain right now. Deepanshu is highly skilled in Django, Flask, APIs and Python. Please email him at deepanshuchauhan2244@gmail.com!");
            }, 800);
        }
    }

    // --- Helper: Get CSRF Token ---
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // --- 6. Event Listeners ---
    if (chatForm) {
        chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const text = chatInput.value.trim();
            if (text) {
                sendMessage(text);
                chatInput.value = '';
            }
        });
    }

    // Sidebar starter questions
    quickQBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const question = btn.getAttribute('data-question');
            if (question) {
                sendMessage(question);
            }
        });
    });

    // --- 7. Greeting ---
    appendMessage(
        'ai', 
        "Hello! I am Deepanshu Assistant. I can answer any questions you have about his skills, education, experience, achievements, or projects.<br/><br/>How can I help you today?", 
        true
    );
});
