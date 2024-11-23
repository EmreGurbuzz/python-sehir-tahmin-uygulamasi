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

document.getElementById('city').addEventListener('input', function() {
    const input = this.value.toLowerCase();
    const dropdown = document.getElementById('city-dropdown');
    dropdown.innerHTML = '';
    fetch('/static/cities.json')
        .then(response => response.json())
        .then(data => {
            const cities = data.cities;
            cities.forEach(city => {
                if (city.name.toLowerCase().includes(input)) {
                    const option = document.createElement('a');
                    option.className = 'dropdown-item';
                    option.textContent = city.name;
                    option.addEventListener('click', function() {
                        document.getElementById('city').value = city.name;
                        dropdown.innerHTML = '';
                    });
                    dropdown.appendChild(option);
                }
            });
            if (dropdown.children.length > 0) {
                dropdown.classList.add('show');
            } else {
                dropdown.classList.remove('show');
            }
        })
        .catch(error => console.error('Error:', error));
});