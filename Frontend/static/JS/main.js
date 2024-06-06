let subDropdown = document.getElementById('subDropdown')

function toggleMenu() {
    subDropdown.classList.toggle('open-menu')
}


document.addEventListener('DOMContentLoaded', function () {
    const sidebarLinks = document.querySelectorAll('.sidebar-link');

    sidebarLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            const submenu = this.querySelector('.submenu');
            const isOpen = submenu.style.display === 'block';
            closeAllSubmenus();
            if (!isOpen) {
                submenu.style.display = 'block';
            }
            event.stopPropagation(); // Evitar que el evento se propague al elemento padre (sidebar-link)
        });
    });

    // Evitar que se cierre el submenú al hacer clic dentro de él
    const submenus = document.querySelectorAll('.submenu');
    submenus.forEach(submenu => {
        submenu.addEventListener('click', function (event) {
            event.stopPropagation(); // Evitar que el evento se propague al elemento padre (sidebar-link)
        });
    });

    document.addEventListener('click', function (event) {
        const isClickInsideSidebar = document.querySelector('.sidebar').contains(event.target);
        if (!isClickInsideSidebar) {
            closeAllSubmenus();
        }
    });
});

function closeAllSubmenus() {
    const submenus = document.querySelectorAll('.submenu');
    submenus.forEach(submenu => {
        submenu.style.display = 'none';
    });
}

const paginationActivos = document.getElementById('pagination-activos');
const paginationInactivos = document.getElementById('pagination-inactivos');

paginationActivos.addEventListener('click', function (event) {
    event.stopPropagation();
});

paginationInactivos.addEventListener('click', function (event) {
    event.stopPropagation();
});



const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});
loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});







// exportar tabla a formato exel

function ExportToExcel(type, fn, dl) {
    var elt = document.getElementById('myTable');
    var wb = XLSX.utils.table_to_book(elt, { sheet: "sheet1" });
    return dl ?
      XLSX.write(wb, { bookType: type, bookSST: true, type: 'base64' }):
      XLSX.writeFile(wb, fn || ('Reporte-SmarkLink.' + (type || 'xlsx')));
 }