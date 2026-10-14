function setPrompt(text) {
    document.getElementById('user-input').value = text;
}

async function sendMessage() {
    const inputField = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const modelSelect = document.getElementById('model-select').value;
    const promptText = inputField.value.trim();

    if (!promptText) return;

    // แสดงข้อความฝั่งผู้ใช้
    chatBox.innerHTML += `<div class="message user">${escapeHtml(promptText)}</div>`;
    inputField.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;

    // สร้างกล่องข้อความรอคำตอบจาก AI พร้อมจับเวลา
    const aiMessageId = 'ai-msg-' + Date.now();
    chatBox.innerHTML += `<div class="message ai" id="${aiMessageId}"><b>${modelSelect}:</b> กำลังคิด...</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    const startTime = performance.now();

    try {
        const response = await fetch('http://localhost:11434/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: modelSelect,
                messages: [{ role: 'user', content: promptText }],
                stream: false
            })
        });

        const data = await response.json();
        const endTime = performance.now();
        const duration = ((endTime - startTime) / 1000).toFixed(2);

        const aiReply = data.message ? data.message.content : 'ไม่พบข้อมูลตอบกลับ';

        // อัปเดตข้อความและเวลาที่ใช้
        document.getElementById(aiMessageId).innerHTML = `
            <b>${modelSelect}:</b><br>${escapeHtml(aiReply)}
            <span class="time-tag">⏱️ เวลาประมวลผล: ${duration} วินาที</span>
        `;
    } catch (error) {
        document.getElementById(aiMessageId).innerHTML = `<b>${modelSelect}:</b><br>❌ เชื่อมต่อ Ollama ไม่สำเร็จ (ตรวจสอบว่ารัน Docker อยู่ไหม)`;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

function escapeHtml(text) {
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
