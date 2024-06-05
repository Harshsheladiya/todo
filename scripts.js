document.addEventListener('DOMContentLoaded', function() {
    flatpickr("#dueDateInput", {
        enableTime: false,
        dateFormat: "Y-m-d",
    });
    flatpickr("#dueTimeInput", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        time_24hr: true,
    });
    fetchTasks();
});

function fetchTasks() {
    fetch('/tasks')
        .then(response => response.json())
        .then(data => {
            const taskList = document.getElementById('taskList');
            taskList.innerHTML = '';
            data.forEach(task => { // Removed 'index' parameter
                const li = document.createElement('li');
                li.className = task.completed ? 'completed' : '';
                li.innerHTML = `
                    <span>${task.task} <br><small>(Due: ${task.due_date || 'No due date'})</small></span>
                    <div>
                        <button onclick="completeTask(${task.id})">Complete</button> <!-- Pass task id -->
                        <button class="delete" onclick="deleteTask(${task.id})">Delete</button> <!-- Pass task id -->
                    </div>
                `;
                taskList.appendChild(li);
            });
        });
}


function addTask() {
    const taskInput = document.getElementById('taskInput');
    const dueDateInput = document.getElementById('dueDateInput');
    const dueTimeInput = document.getElementById('dueTimeInput');
    const task = taskInput.value.trim();
    let due_time = dueTimeInput.value.trim();

    // Convert time to AM/PM format
    const hour = parseInt(due_time.split(':')[0]);
    const am_pm = (hour >= 12) ? 'PM' : 'AM';
    const hour_12 = (hour % 12 === 0) ? 12 : hour % 12;
    const minute = due_time.split(':')[1];
    due_time = hour_12 + ':' + minute + ' ' + am_pm;

    const due_date = dueDateInput.value + " " + due_time;

    if (task) {
        // Check if the due date is in the future
        const dueDateTime = new Date(due_date);
        const now = new Date();

        if (dueDateTime > now) {
            fetch('/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ task, due_date })
            })
            .then(response => response.json())
            .then(data => {
                taskInput.value = '';
                dueDateInput.value = '';
                dueTimeInput.value = '';
                fetchTasks();
            });
        } else {
            alert('Please select a future due date and time.');
        }
    } else {
        alert('Please enter a task.');
    }
}



function completeTask(taskId) {
    fetch(`/tasks/${taskId}/complete`, {
        method: 'PUT'
    })
    .then(response => response.json())
    .then(data => {
        fetchTasks();
    });
}

function deleteTask(taskId) {
    fetch(`/tasks/${taskId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        fetchTasks();
    });
}
