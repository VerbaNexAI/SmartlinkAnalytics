document.addEventListener('DOMContentLoaded', function () {
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    const submenus = document.querySelectorAll('.submenu');

    sidebarLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            const submenu = this.querySelector('.submenu');
            const isOpen = submenu.style.display === 'block';
            closeAllSubmenus();
            if (!isOpen) {
                submenu.style.display = 'block';
            }
            event.stopPropagation();
        });
    });

    submenus.forEach(submenu => {
        submenu.addEventListener('click', function (event) {
            event.stopPropagation();
        });
    });


    // Evitar que los clics en la paginación afecten al menú
    const paginationElements = [
        'pagination-inactive',
        'prev-inactive',
        'next-inactive',
        'pagination-active',
        'prev-active',
        'next-active'
    ];

    paginationElements.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('click', function (event) {
                event.stopPropagation();
            });
        }
    });
});

function toggleMenu() {
    let subDropdown = document.getElementById('subDropdown');
    if (subDropdown) {
        subDropdown.classList.toggle('open-menu');
    }
}

function closeAllSubmenus() {
    const submenus = document.querySelectorAll('.submenu');
    submenus.forEach(submenu => {
        submenu.style.display = 'none';
    });
}

function ExportToExcel(type, fn, dl) {
    var elt = document.getElementById('myTable');
    if (elt) {
        var wb = XLSX.utils.table_to_book(elt, { sheet: "sheet1" });
        return dl ?
            XLSX.write(wb, { bookType: type, bookSST: true, type: 'base64' }) :
            XLSX.writeFile(wb, fn || ('Reporte-SmarkLink.' + (type || 'xlsx')));
    }
}
