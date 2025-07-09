document.addEventListener("DOMContentLoaded", function () {
  loadAllEmployees();
});

function addEmployee(event) {
  event.preventDefault();

  const form = event.target;
  const isEdit = form.dataset.editId;

  const employeeData = {
    name: document.getElementById("name").value.trim(),
    address: document.getElementById("address").value.trim(),
    age: document.getElementById("age").value,
    gender: document.getElementById("gender").value,
    position: document.getElementById("position").value.trim(),
    username: document.getElementById("username").value.trim(),
    password: document.getElementById("password").value.trim(),
    role: document.getElementById("role").value
  };

  if (isEdit) {
    employeeData.id = form.dataset.editId;
  }

  if (
    !employeeData.name ||
    !employeeData.address ||
    !employeeData.age ||
    !employeeData.gender ||
    !employeeData.position ||
    !employeeData.username ||
    (!isEdit && !employeeData.password) ||
    !employeeData.role
  ) {
    alert("Please fill in all required fields");
    return false;
  }

  const url = isEdit ? "/edit-employee" : "/add-employee";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(employeeData),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert(data.message);
        form.reset();
        if (isEdit) {
          cancelEdit();
        }
        loadAllEmployees();
      } else {
        alert(
          "Error: " +
            (data.error || `Failed to ${isEdit ? "update" : "add"} employee`)
        );
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert(
        `Failed to ${isEdit ? "update" : "add"} employee. Please try again.`
      );
    });

  return false;
}

function loadAllEmployees() {
  fetch("/get-all-employees")
    .then((response) => {
      if (!response.ok) {
        return response.json().then((errData) => {
          throw new Error(
            errData.error || `HTTP error! status: ${response.status}`
          );
        });
      }
      return response.json();
    })
    .then((data) => {
      if (data.success) {
        const tbody = document.getElementById("employeeTableBody");
        tbody.innerHTML = "";

        if (!data.employees || data.employees.length === 0) {
          tbody.innerHTML = `
                        <tr>
                            <td colspan="9" class="text-center">No employees found</td>
                        </tr>
                    `;
          return;
        }

        data.employees.forEach((employee) => {
          tbody.innerHTML += `
                    <tr data-id="${employee.id}">
                        <td>${employee.id || ""}</td>
                        <td data-field="name">${employee.name || ""}</td>
                        <td data-field="address">${employee.address || ""}</td>
                        <td data-field="age">${employee.age || ""}</td>
                        <td data-field="gender">${employee.gender || ""}</td>
                        <td data-field="position">${employee.position || ""}</td>
                        <td data-field="username">${employee.username || ""}</td>
                        <td data-field="role">${employee.role || ""}</td>
                        <td>
                            <button class="btn btn-success btn-sm me-1 ml-2" onclick="editEmployee('${employee.id}')">Edit</button>
                            <button class="btn btn-success btn-sm" onclick="deleteEmployee('${employee.id}')">Delete</button>
                        </td>
                    </tr>
                    `;
        });
      } else {
        throw new Error(data.error || "Failed to load employees");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      const tbody = document.getElementById("employeeTableBody");
      tbody.innerHTML = `
                <tr>
                    <td colspan="9" class="text-center text-danger">
                        Error loading employees: ${error.message}
                    </td>
                </tr>
            `;
    });
}

function editEmployee(id) {
  const row = document.querySelector(`tr[data-id="${id}"]`);
  const employee = {
    id: id,
    name: row.querySelector('[data-field="name"]').textContent,
    address: row.querySelector('[data-field="address"]').textContent,
    age: row.querySelector('[data-field="age"]').textContent,
    gender: row.querySelector('[data-field="gender"]').textContent,
    position: row.querySelector('[data-field="position"]').textContent,
    username: row.querySelector('[data-field="username"]').textContent,
    role: row.querySelector('[data-field="role"]').textContent
  };

  document.getElementById("name").value = employee.name;
  document.getElementById("address").value = employee.address;
  document.getElementById("age").value = employee.age;
  document.getElementById("gender").value = employee.gender;
  document.getElementById("position").value = employee.position;
  document.getElementById("username").value = employee.username;
  document.getElementById("role").value = employee.role;

  document.getElementById("password").value = "";
  document.getElementById("password").removeAttribute("required");

  const form = document.getElementById("addEmployeeForm");
  const submitBtn = form.querySelector('button[type="submit"]');
  submitBtn.textContent = "Update Employee";
  form.dataset.editId = id;

  if (!form.querySelector(".btn-secondary")) {
    const cancelBtn = document.createElement("button");
    cancelBtn.className = "btn btn-secondary mt-2 ms-2";
    cancelBtn.textContent = "Cancel";
    cancelBtn.onclick = cancelEdit;
    submitBtn.parentNode.appendChild(cancelBtn);
  }
}

function cancelEdit() {
  const form = document.getElementById("addEmployeeForm");
  form.reset();
  delete form.dataset.editId;

  const submitBtn = form.querySelector('button[type="submit"]');
  submitBtn.textContent = "Add Employee";

  document.getElementById("password").setAttribute("required", "");

  const cancelBtn = form.querySelector(".btn-secondary");
  if (cancelBtn) cancelBtn.remove();
}

function deleteEmployee(id) {
  if (confirm("Are you sure you want to delete this employee?")) {
    fetch("/delete-employee", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id: id }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert(data.message);
          loadAllEmployees();
        } else {
          alert("Error: " + (data.error || "Failed to delete employee"));
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Failed to delete employee. Please try again.");
      });
  }
}

function logout() {
  fetch("/logout", {
    method: "POST",
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        window.location.href = data.redirect;
      }
    })
    .catch((error) => console.error("Error:", error));
}