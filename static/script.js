document.getElementById('hint-button').addEventListener('click', function() {
    fetch('/hint')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                const hintList = document.getElementById('hints-list');
                const newHint = document.createElement('li');
                newHint.className = 'list-group-item';
                newHint.textContent = data.hint;
                hintList.appendChild(newHint);
                // Update hint count on the button
                const hintButton = document.getElementById('hint-button');
                const hintCount = parseInt(hintButton.textContent.match(/\d+/)[0]) - 1;
                hintButton.textContent = `İpucu Al (${hintCount})`;
            }
        })
        .catch(error => console.error('Error:', error));
});

// Remove the form submission check



