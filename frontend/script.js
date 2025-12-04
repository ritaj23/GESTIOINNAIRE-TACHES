// ========================================
// UTILISATEUR
// ========================================

// LOGIN / REGISTER
document.getElementById("registerForm")?.addEventListener("submit", async function(e){
    e.preventDefault();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if(!username || !password) return alert("Veuillez remplir tous les champs.");

    try {
        const res = await fetch("http://127.0.0.1:8000/api/register", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username, password})
        });
        const data = await res.json();
        alert(data.message || data.error);
        if(data.message) window.location.href = "login.html";
    } catch(err){
        alert("Erreur lors de l'inscription");
        console.error(err);
    }
});

document.getElementById("loginForm")?.addEventListener("submit", async function(e){
    e.preventDefault();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if(!username || !password) return alert("Veuillez remplir tous les champs.");

    try {
        const res = await fetch("http://127.0.0.1:8000/api/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username, password})
        });
        const data = await res.json();
        if(data.message){
            localStorage.setItem("username", username);
            localStorage.setItem("token", data.token);
            window.location.href = "mes_taches.html";
        } else {
            alert(data.error);
        }
    } catch(err){
        alert("Erreur lors de la connexion");
        console.error(err);
    }
});

// ========================================
// MES TÂCHES
// ========================================
const username = localStorage.getItem("username");
const token = localStorage.getItem("token");

if(window.location.pathname.includes("mes_taches.html") && !token){
    window.location.href = "login.html";
}

// Déconnexion
document.getElementById("logoutBtn")?.addEventListener("click", ()=>{
    localStorage.clear();
    window.location.href = "login.html";
});

// Charger tâches
async function loadTasks(){
    try {
        const res = await fetch("http://127.0.0.1:8000/api/tasks", {
            headers: { "Authorization": `Bearer ${token}` }
        });
        if(!res.ok) throw new Error("Impossible de récupérer les tâches");
        const tasks = await res.json();

        const tbody = document.querySelector("#tasksTable tbody");
        tbody.innerHTML = "";

        tasks.forEach(task => {
            if(task.owner === username || (task.collaborators && task.collaborators.includes(username))){
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${task.title}</td>
                    <td>${task.description}</td>
                    <td>${task.owner}</td>
                    <td>${(task.collaborators || []).join(", ")}</td>
                    <td>${task.completed ? "Complété" : "En cours"}</td>
                    <td>
                        <button class="editBtn" data-id="${task._id}">Modifier</button>
                        <button class="deleteBtn" data-id="${task._id}">Supprimer</button>
                    </td>
                `;
                tbody.appendChild(tr);
            }
        });

        attachTaskButtons();
    } catch(err){
        console.error(err);
        alert("Erreur lors du chargement des tâches");
    }
}

// CRUD buttons
function attachTaskButtons(){
    document.querySelectorAll(".deleteBtn").forEach(btn=>{
        btn.addEventListener("click", async e=>{
            const id = e.target.dataset.id;
            if(!confirm("Voulez-vous vraiment supprimer cette tâche ?")) return;
            try {
                const res = await fetch(`http://127.0.0.1:8000/api/tasks/${id}`, {
                    method: "DELETE",
                    headers: { "Authorization": `Bearer ${token}` }
                });
                if(res.ok) {
                    alert("Tâche supprimée avec succès");
                    loadTasks();
                }
            } catch(err){
                console.error(err);
                alert("Erreur lors de la suppression");
            }
        });
    });

    document.querySelectorAll(".editBtn").forEach(btn=>{
        btn.addEventListener("click", async e=>{
            const id = e.target.dataset.id;
            const newTitle = prompt("Nouveau titre:");
            if(!newTitle) return alert("Le titre est obligatoire");
            const newDesc = prompt("Nouvelle description:") || "";
            const completed = confirm("Tâche complétée ?");

            try {
                const res = await fetch(`http://127.0.0.1:8000/api/tasks/${id}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    },
                    body: JSON.stringify({title:newTitle, description:newDesc, completed})
                });
                if(res.ok){
                    alert("Tâche mise à jour avec succès");
                    loadTasks();
                }
            } catch(err){
                console.error(err);
                alert("Erreur lors de la mise à jour");
            }
        });
    });
}

// Ajouter tâche
document.getElementById("addTaskBtn")?.addEventListener("click", async ()=>{
    const title = prompt("Titre de la tâche:");
    if(!title) return alert("Le titre est obligatoire");

    const description = prompt("Description:") || "";
    const collaboratorsInput = prompt("Collaborateurs (séparés par des virgules):") || "";
    const collaborators = collaboratorsInput.split(",").map(c=>c.trim()).filter(c=>c);

    try {
        const res = await fetch("http://127.0.0.1:8000/api/tasks", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({title, description, collaborators})
        });
        const data = await res.json();
        if(data.message){
            alert("Tâche ajoutée avec succès");
            loadTasks();
        } else if(data.error){
            alert(data.error);
        }
    } catch(err){
        console.error(err);
        alert("Erreur lors de l'ajout de la tâche");
    }
});

// Initial load
if(window.location.pathname.includes("mes_taches.html")) loadTasks();
