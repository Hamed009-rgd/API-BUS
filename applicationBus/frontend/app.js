let token = "";
const API_URL = "http://127.0.0.1:8000";

// LOGIN
async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    });

    const data = await res.json();
    if (res.ok) {
        token = data.access_token;
        alert("Connecté !");
    } else {
        alert(data.detail);
    }
}

// BUS
async function getBus() {
    const res = await fetch(`${API_URL}/bus`, {
        headers: {"Authorization": `Bearer ${token}`}
    });
    const bus = await res.json();
    const list = document.getElementById("busList");
    list.innerHTML = "";
    bus.forEach(b => {
        const li = document.createElement("li");
        li.innerText = `Bus #${b.id} - ${b.numero} (Capacité: ${b.capacite})`;
        list.appendChild(li);
    });
}

async function addBus() {
    const numero = document.getElementById("busNumero").value;
    const capacite = parseInt(document.getElementById("busCapacite").value);

    await fetch(`${API_URL}/bus`, {
        method: "POST",
        headers: {"Content-Type": "application/json", "Authorization": `Bearer ${token}`},
        body: JSON.stringify({numero, capacite})
    });
    getBus();
}

// CHAUFFEUR
async function getChauffeurs() {
    const res = await fetch(`${API_URL}/chauffeur`, {headers: {"Authorization": `Bearer ${token}`}});
    const chauffeurs = await res.json();
    const list = document.getElementById("chauffeurList");
    list.innerHTML = "";
    chauffeurs.forEach(c => {
        const li = document.createElement("li");
        li.innerText = `${c.id} - ${c.nom} | Salaire: ${c.salaire_base} | Bus ID: ${c.bus_id}`;
        list.appendChild(li);
    });
}

async function addChauffeur() {
    const nom = document.getElementById("chauffeurNom").value;
    const salaire_base = parseFloat(document.getElementById("chauffeurSalaire").value);
    const bus_id = parseInt(document.getElementById("chauffeurBusId").value);

    await fetch(`${API_URL}/chauffeur`, {
        method: "POST",
        headers: {"Content-Type": "application/json", "Authorization": `Bearer ${token}`},
        body: JSON.stringify({nom, salaire_base, bus_id})
    });
    getChauffeurs();
}

// CONTROLEUR
async function getControleurs() {
    const res = await fetch(`${API_URL}/controleur`, {headers: {"Authorization": `Bearer ${token}`}});
    const controleurs = await res.json();
    const list = document.getElementById("controleurList");
    list.innerHTML = "";
    controleurs.forEach(c => {
        const li = document.createElement("li");
        li.innerText = `${c.id} - ${c.nom} | Salaire: ${c.salaire_base} | Bus ID: ${c.bus_id}`;
        list.appendChild(li);
    });
}

async function addControleur() {
    const nom = document.getElementById("controleurNom").value;
    const salaire_base = parseFloat(document.getElementById("controleurSalaire").value);
    const bus_id = parseInt(document.getElementById("controleurBusId").value);

    await fetch(`${API_URL}/controleur`, {
        method: "POST",
        headers: {"Content-Type": "application/json", "Authorization": `Bearer ${token}`},
        body: JSON.stringify({nom, salaire_base, bus_id})
    });
    getControleurs();
}

// DEPENSE
async function getDepenses() {
    const res = await fetch(`${API_URL}/depense`, {headers: {"Authorization": `Bearer ${token}`}});
    const depenses = await res.json();
    const list = document.getElementById("depenseList");
    list.innerHTML = "";
    depenses.forEach(d => {
        const li = document.createElement("li");
        li.innerText = `${d.id} - ${d.nom} | Montant: ${d.montant}`;
        list.appendChild(li);
    });
}

async function addDepense() {
    const nom = document.getElementById("depenseNom").value;
    const montant = parseFloat(document.getElementById("depenseMontant").value);

    await fetch(`${API_URL}/depense`, {
        method: "POST",
        headers: {"Content-Type": "application/json", "Authorization": `Bearer ${token}`},
        body: JSON.stringify({nom, montant})
    });
    getDepenses();
}

// FINANCE
async function getFinance() {
    const res = await fetch(`${API_URL}/finance/resume`, {headers: {"Authorization": `Bearer ${token}`}});
    const data = await res.json();
    document.getElementById("finance").innerText = `Total salaires: ${data.total_salaire}, Total dépenses: ${data.total_depenses}, Bénéfice: ${data.benefice}`;
}

// HISTORIQUE
async function getHistorique() {
    const res = await fetch(`${API_URL}/historique`, {headers: {"Authorization": `Bearer ${token}`}});
    const data = await res.json();
    document.getElementById("historique").innerText = JSON.stringify(data, null, 2);
}