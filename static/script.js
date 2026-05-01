let allParagraphs = [];
let currentIdx = 0;

async function askAI() {
    const input = document.getElementById('user-input');
    const container = document.getElementById('response-container');
    const header = document.getElementById('title-header');
    const msg = input.value.trim();

    if (!msg) return;

    // Thu nhỏ tiêu đề khi bắt đầu chat
    header.style.fontSize = "18px";
    header.style.marginBottom = "10px";

    container.innerHTML = `<p style="color: #888;">AI đang tìm kiếm thông tin...</p>`;
    input.value = "";

    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg })
        });
        const data = await res.json();

        if (data.error) {
            container.innerHTML = `<p style="color: #ff6b6b;">${data.error}</p>`;
        } else {
            allParagraphs = data.paragraphs;
            currentIdx = 3;
            container.innerHTML = `<a href="${data.url}" target="_blank" class="source-link">Nguồn: ${data.url}</a>`;
            displayBatch(allParagraphs.slice(0, 3));
        }
    } catch (e) {
        container.innerHTML = `<p style="color: #ff6b6b;">Lỗi kết nối Server.</p>`;
    }
}

function displayBatch(batch) {
    const container = document.getElementById('response-container');
    batch.forEach(text => {
        const p = document.createElement('p');
        p.className = 'paragraph';
        p.innerText = text;
        container.appendChild(p);
    });

    if (currentIdx < allParagraphs.length) {
        const btn = document.createElement('button');
        btn.className = 'read-more-btn';
        btn.innerText = "Xem thêm nội dung...";
        btn.onclick = () => {
            btn.remove();
            const nextBatch = allParagraphs.slice(currentIdx, currentIdx + 3);
            currentIdx += 3;
            displayBatch(nextBatch);
        };
        container.appendChild(btn);
    }
}

document.getElementById('send-btn').onclick = askAI;
document.getElementById('user-input').onkeypress = (e) => { if (e.key === 'Enter') askAI(); };