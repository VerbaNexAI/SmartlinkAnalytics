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

    document.addEventListener('click', function (event) {
        const isClickInsideSidebar = document.querySelector('.sidebar').contains(event.target);
        if (!isClickInsideSidebar) {
            closeAllSubmenus();
        }
    });

    paginationActivos.addEventListener('click', function (event) {
        event.stopPropagation();
    });

    paginationInactivos.addEventListener('click', function (event) {
        event.stopPropagation();
    });
});

function toggleMenu() {
    let subDropdown = document.getElementById('subDropdown');
    subDropdown.classList.toggle('open-menu');
}

function closeAllSubmenus() {
    const submenus = document.querySelectorAll('.submenu');
    submenus.forEach(submenu => {
        submenu.style.display = 'none';
    });
}

function ExportToExcel(type, fn, dl) {
    var elt = document.getElementById('myTable');
    var wb = XLSX.utils.table_to_book(elt, { sheet: "sheet1" });
    return dl ?
        XLSX.write(wb, { bookType: type, bookSST: true, type: 'base64' }) :
        XLSX.writeFile(wb, fn || ('Reporte-SmarkLink.' + (type || 'xlsx')));
}
