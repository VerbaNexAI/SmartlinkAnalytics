// URLs de la API
const apiUrl = 'http://192.168.0.226:5200/api/project';
const postUrl = 'http://192.168.0.226:5200/api/view';

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
    const projects = [projectName]; // Adjust to match the expected structure
    console.log(projects); // Verify the structure in the console

    fetch('http://192.168.0.226:5200/api/view', { // Ensure the URL is correct
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ projects: projects }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data); // Verify the response in the console
        renderTable(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
};



const renderTable = (data) => {
    // Crear la tabla
    const table = $('<table>')
        .attr('id', 'example')
        .addClass('table table-striped table-bordered second')
        .css('width', '100%');

    // Cabecera de la tabla
    const headerRow = $('<thead>').appendTo(table);
    const headerCells = $('<tr>').appendTo(headerRow);

    Object.keys(data[0]).forEach(key => {
        const th = $('<th>').text(key);

        // Establecer texto del tooltip
        let tooltipText = '';
        if (key.toLowerCase() === 'score') {
            tooltipText = 'Texto descriptivo para Score.';
        } 
        else if (key.toLowerCase() === 'description') {
            tooltipText = 'Texto descriptivo para Description.';
        }
        else if (key.toLowerCase() === 'sp_modelitemid') {
            tooltipText = 'Texto descriptivo para SP_ModelItemID.';
        }
        else if (key.toLowerCase() === 'path') {
            tooltipText = 'Texto descriptivo para Path.';
        }
        else if (key.toLowerCase() === 'drawing_name') {
            tooltipText = 'Texto descriptivo para Drawing_Name.';
        }
        else if (key.toLowerCase() === 'isapproved') {
            tooltipText = 'Texto descriptivo para IsApproved.';
        }
        else if (key.toLowerCase() === 'inconsistencystatus') {
            tooltipText = 'Texto descriptivo para InconsistencyStatus.';
        }
        else if (key.toLowerCase() === 'severity') {
            tooltipText = 'Texto descriptivo para Severity.';
        }

        // Si hay texto de tooltip, asignar eventos
        if (tooltipText) {
            th.hover(function(event) {
                showTooltip(event, tooltipText);
            }, function() {
                hideTooltip();
            });
        }

        th.appendTo(headerCells);
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

// Funciones para mostrar y ocultar el tooltip personalizado
function showTooltip(event, text) {
    const tooltip = $('<div>')
        .addClass('tooltip-custom')
        .text(text)
        .css({
            top: event.pageY + 20,
            left: event.pageX + 20
        })
        .appendTo('body');
    tooltip.fadeIn('fast');
}

function hideTooltip() {
    $('.tooltip-custom').remove();
}


// Renderizar la lista de proyectos activos o inactivos
const renderProjectsList = (data, element, paginationId) => {
    const items = data.map(item => {
        const listItem = document.createElement('li');
        listItem.textContent = item.name;
        listItem.addEventListener('click', () => {
            sendPostRequest(item.name); 
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
                sendPostRequest(items[i].textContent);
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
