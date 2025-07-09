document.addEventListener('DOMContentLoaded', function() {
    loadEmployeeInfo();
});

function loadEmployeeInfo() {
    fetch('/get-employee-info')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const info = data.employee_info;
                document.getElementById('username').textContent = info.username || '';
                document.getElementById('name').textContent = info.name || '';
                document.getElementById('address').textContent = info.address || '';
                document.getElementById('age').textContent = info.age || '';
                document.getElementById('gender').textContent = info.gender || '';
                document.getElementById('position').textContent = info.position || '';
            } else {
                alert('Error loading employee information: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to load employee information');
        });
}

function logout() {
    fetch('/logout', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect;
        }
    })
    .catch(error => console.error('Error:', error));
}