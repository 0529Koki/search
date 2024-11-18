// エリアをクリックしたときに地域名の詳細を表示/非表示にする
document.querySelectorAll('.region-btn').forEach(button => {
    button.addEventListener('click', () => {
        const area = button.nextElementSibling;
        if (area.style.display === 'block') {
            area.style.display = 'none';
        } else {
            area.style.display = 'block';
        }
    });
});
