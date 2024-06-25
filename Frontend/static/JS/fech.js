// URLs de la API
const apiUrl = 'http://127.0.0.1:8000/api/project';
const apiUrlInactivos = 'http://127.0.0.1:8000/api/project/inactive';
const postUrl = 'http://127.0.0.1:8000/api/view';

// Elementos del DOM
const dataList = document.getElementById('data-list');
const dataListInactivos = document.getElementById('data_list_inactive');
const table = document.getElementById('myTable');
const itemsPerPage = 10; 

// Manejo de la respuesta de la API
const handleResponse = (response, element, paginationId) => {
    if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
    }
    return response.json().then(data => {
        console.log(data);
        const items = data.map(item => {
            const listItem = document.createElement('li');
            const icon = document.createElement('i');
            icon.className = "fa-solid fa-folder";
            listItem.appendChild(icon);
            const text = document.createTextNode(` ${item.PROYECTO}`);
            listItem.appendChild(text);
            listItem.addEventListener('click', () => {
                sendPostRequest(item.PROYECTO); // Enviar solo el nombre del proyecto
            });

            return listItem;
        });
        paginate(items, element, paginationId);
    });
};

// Enviar solicitud POST
const sendPostRequest = (project) => {
    fetch(postUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ project: project }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        renderTable(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
};

// Renderizar la tabla
const renderTable = (data) => {
    table.innerHTML = '';
    const headerRow = document.createElement('tr');
    for (const key in data[0]) {
        const th = document.createElement('th');
        th.textContent = key;
        headerRow.appendChild(th);
    }
    table.appendChild(headerRow);
    data.forEach(item => {
        const row = document.createElement('tr');
        for (const key in item) {
            const cell = document.createElement('td');
            cell.textContent = item[key];
            row.appendChild(cell);
        }
        table.appendChild(row);
    });
};

// Fetch datos activos
fetch(apiUrl)
    .then(response => handleResponse(response, dataList, 'active'))
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        const errorItem = document.createElement('li');
        errorItem.textContent = 'Error fetching data';
        errorItem.className = 'error';
        dataList.appendChild(errorItem);
    });

// Fetch datos inactivos
fetch(apiUrlInactivos)
    .then(response => handleResponse(response, dataListInactivos, 'inactive'))
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        const errorItem = document.createElement('li');
        errorItem.textContent = 'Error fetching data';
        errorItem.className = 'error';
        dataListInactivos.appendChild(errorItem);
    });

// Paginación
const paginate = (items, listElement, paginationId) => {
    let currentPage = 1;
    const totalPages = Math.ceil(items.length / itemsPerPage);

    const renderPage = (page) => {
        listElement.innerHTML = '';
        const start = (page - 1) * itemsPerPage;
        const end = Math.min(page * itemsPerPage, items.length);
        for (let i = start; i < end; i++) {
            listElement.appendChild(items[i]);
        }
        updatePaginationButtons();
    };

    const updatePaginationButtons = () => {
        const prevButton = document.getElementById(`prev-${paginationId}`);
        const nextButton = document.getElementById(`next-${paginationId}`);
        prevButton.disabled = currentPage === 1;
        nextButton.disabled = currentPage === totalPages;
    };

    document.getElementById(`prev-${paginationId}`).addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            renderPage(currentPage);
        }
    });

    document.getElementById(`next-${paginationId}`).addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage++;
            renderPage(currentPage);
        }
    });

    renderPage(currentPage);
};