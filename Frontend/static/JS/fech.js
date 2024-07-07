// URLs de la API
const apiUrl = 'http://127.0.0.1:8000/api/project';
const apiUrlInactivos = 'http://127.0.0.1:8000/api/project/inactive';
const postUrl = 'http://127.0.0.1:8000/api/view';

// Elementos del DOM
const itemsPerPage = 10;

// Manejo de la respuesta de la API para proyectos
const handleProjectsResponse = (response, element, paginationId) => {
    if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
    }
    return response.json().then(data => {
        console.log(data); // Verifica los datos recibidos en la consola
        renderProjectsList(data, element, paginationId);
    });
};

// Manejo de la respuesta de la API para solicitud POST
const handlePostResponse = (response) => {
    if (!response.ok) {
        return response.json().then(errorData => {
            throw new Error(`Network response was not ok: ${response.statusText}. ${errorData.error || ''}`);
        });
    }
    return response.json();
};

const sendPostRequest = (projectName) => {
    const projects = [{ project_id: projectName }]; // Ajustar según la estructura esperada
    fetch(postUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ projects: projects }),
    })
    .then(handlePostResponse)
    .then(data => {
        console.log('Success:', data); // Verifica la respuesta del POST en la consola
        renderTable(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
};

// Renderizar la tabla con los datos recibidos
const renderTable = (data) => {
    // Crear la tabla
    const table = $('<table>').attr('id', 'example').addClass('table table-striped table-bordered second').css('width', '100%');

    // Cabecera de la tabla
    const headerRow = $('<thead>').appendTo(table);
    const headerCells = $('<tr>').appendTo(headerRow);
    Object.keys(data[0]).forEach(key => {
        $('<th>').text(key).appendTo(headerCells);
    });

    // Cuerpo de la tabla
    const tbody = $('<tbody>').appendTo(table);
    data.forEach(item => {
        const row = $('<tr>').appendTo(tbody);
        Object.values(item).forEach(value => {
            $('<td>').text(value).appendTo(row);
        });
    });

    // Añadir la tabla al contenedor .table-responsive
    $('.table-responsive').empty().append(table);

    $(document).ready(function() {
        $('.reporte').css('background-color', '#fff');
    });

    // Inicializar DataTables
    $('#example').DataTable({
        dom: '<"row"<"col-md-6"l><"col-md-6"f>><"row"<"col-md-12"B>>rtip', // Alineación de botones y barra de búsqueda
        buttons: [
            'copy', 'excel', 'pdf', 'print'
        ]
    });
};

// Renderizar la lista de proyectos activos o inactivos
const renderProjectsList = (data, element, paginationId) => {
    const items = data.map(item => {
        const listItem = document.createElement('li');
        listItem.textContent = item.name;
        listItem.addEventListener('click', () => {
            sendPostRequest(item.name); // Enviar solo el nombre del proyecto al hacer clic
        });
        return listItem;
    });

    paginate(items, element, paginationId);
};

// Fetch datos activos
fetch(apiUrl)
    .then(response => handleProjectsResponse(response, document.getElementById('data-list'), 'active'))
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        const errorItem = document.createElement('li');
        errorItem.textContent = 'Error fetching data';
        errorItem.className = 'error';
        document.getElementById('data-list').appendChild(errorItem);
    });

// Fetch datos inactivos
fetch(apiUrlInactivos)
    .then(response => handleProjectsResponse(response, document.getElementById('data_list_inactive'), 'inactive'))
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        const errorItem = document.createElement('li');
        errorItem.textContent = 'Error fetching data';
        errorItem.className = 'error';
        document.getElementById('data_list_inactive').appendChild(errorItem);
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
            const listItem = document.createElement('li');
            listItem.textContent = items[i].textContent;
            listItem.addEventListener('click', () => {
                sendPostRequest(items[i].textContent); // Enviar solo el nombre del proyecto al hacer clic
            });
            listElement.appendChild(listItem);
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
