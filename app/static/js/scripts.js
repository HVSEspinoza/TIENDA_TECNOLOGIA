let selectedCategory = '';
let currentPage = 1;
const rowsPerPage = 10;

function toggleDetails(event, productId) {
    event.preventDefault();
    const detailsRow = document.getElementById(`details-${productId}`);
    if (detailsRow.style.display === 'none' || detailsRow.style.display === '') {
        detailsRow.style.display = 'table-row';
        detailsRow.classList.add('slide-in');
    } else {
        detailsRow.classList.add('slide-out');
        setTimeout(() => {
            detailsRow.style.display = 'none';
            detailsRow.classList.remove('slide-out');
        }, 300);
    }
}

function enviarFormulario() {
    document.getElementById('almacenForm').submit();
}

function toggleCategory(element) {
    const subList = element.parentElement.querySelector('ul');
    if (subList.style.display === 'none' || subList.style.display === '') {
        subList.style.display = 'block';
        element.textContent = '[-]';
    } else {
        subList.style.display = 'none';
        element.textContent = '[+]';
    }
}

function selectCategory(category, event) {
    event.preventDefault();
    // Reemplazar guiones y normalizar
    selectedCategory = category.toLowerCase().trim().replace(/\s*-\s*/g, ' ');
    console.log('Categoría seleccionada:', selectedCategory);
    document.querySelectorAll('.category-tree a').forEach(link => {
        link.classList.remove('selected');
    });
    event.target.classList.add('selected');
    aplicarFiltros();
}

function aplicarFiltros() {
    const input = document.getElementById('searchInput').value.toLowerCase().trim();
    const rows = document.querySelectorAll('#productosTable tbody tr:not(.details-row)');

    console.log('Texto de búsqueda:', input);
    console.log('Categoría seleccionada en aplicarFiltros:', selectedCategory);

    rows.forEach(row => {
        // Verificar si la fila tiene suficientes celdas
        if (row.cells.length < 8) {
            row.style.display = 'none';
            return;
        }

        const description = row.cells[0].textContent.toLowerCase().trim();
        const marca = row.cells[4].textContent.toLowerCase().trim();
        const categoria = row.cells[5].textContent.toLowerCase().trim();
        const almacen = row.cells[6].textContent.toLowerCase().trim();

        console.log('Fila:', { description, marca, categoria, almacen });

        const searchMatch = (
            description.includes(input) ||
            marca.includes(input) ||
            categoria.includes(input) ||
            almacen.includes(input)
        );

        const categoryMatch = selectedCategory === '' || categoria.startsWith(selectedCategory);

        console.log('Coincide con búsqueda:', searchMatch, 'Coincide con categoría:', categoryMatch);

        row.style.display = (searchMatch && categoryMatch) ? '' : 'none';

        const detailsRow = row.nextElementSibling;
        if (detailsRow && detailsRow.classList.contains('details-row')) {
            detailsRow.style.display = row.style.display === 'none' ? 'none' : detailsRow.style.display;
        }
    });

    currentPage = 1;
    updateTable();
    updateProductCount();
}
function buscarProductos() {
    console.log('Evento buscarProductos disparado'); // Depuración
    aplicarFiltros();
}

function filtrarPorCategoria() {
    console.log('Evento filtrarPorCategoria disparado'); // Depuración
    aplicarFiltros();
}

function limpiarFiltros() {
    console.log('Limpiando filtros'); // Depuración
    document.getElementById('searchInput').value = '';
    selectedCategory = '';
    document.querySelectorAll('.category-tree a').forEach(link => {
        link.classList.remove('selected');
    });
    document.getElementById('almacenForm').reset();
    aplicarFiltros();
}

function updateTable() {
    const rows = document.querySelectorAll('#productosTable tbody tr:not(.details-row)');
    const visibleRows = Array.from(rows).filter(row => row.style.display !== 'none');
    const totalRows = visibleRows.length;
    const totalPages = Math.ceil(totalRows / rowsPerPage);

    if (currentPage < 1) currentPage = 1;
    if (currentPage > totalPages) currentPage = totalPages;

    let visibleCount = 0;
    rows.forEach((row, index) => {
        if (row.style.display !== 'none') {
            const shouldShow = visibleCount >= (currentPage - 1) * rowsPerPage && visibleCount < currentPage * rowsPerPage;
            row.style.display = shouldShow ? '' : 'none';
            const detailsRow = row.nextElementSibling;
            if (detailsRow && detailsRow.classList.contains('details-row')) {
                detailsRow.style.display = shouldShow ? detailsRow.style.display : 'none';
            }
            visibleCount++;
        }
    });

    document.getElementById('pageInfo').textContent = `Página ${currentPage} de ${totalPages}`;
    document.querySelector('.pagination button:first-child').disabled = currentPage === 1;
    document.querySelector('.pagination button:last-child').disabled = currentPage === totalPages || totalPages === 0;
}

function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        updateTable();
    }
}

function nextPage() {
    const rows = document.querySelectorAll('#productosTable tbody tr:not(.details-row)');
    const visibleRows = Array.from(rows).filter(row => row.style.display !== 'none');
    const totalPages = Math.ceil(visibleRows.length / rowsPerPage);
    if (currentPage < totalPages) {
        currentPage++;
        updateTable();
    }
}

function updateProductCount() {
    const visibleRows = document.querySelectorAll('#productosTable tbody tr:not(.details-row)[style="display: "]').length;
    document.getElementById('productCount').textContent = `Mostrando ${visibleRows} productos`;
}

const carousels = {};
function moveCarousel(productId, direction) {
    const carousel = document.getElementById(`carousel-${productId}`);
    const track = carousel.querySelector('.carousel-track');
    const cards = track.querySelectorAll('.carousel-card');
    if (!carousels[productId]) {
        carousels[productId] = { currentIndex: 0 };
    }
    let currentIndex = carousels[productId].currentIndex;
    currentIndex += direction;

    if (currentIndex < 0) currentIndex = 0;
    if (currentIndex >= cards.length) currentIndex = cards.length - 1;

    carousels[productId].currentIndex = currentIndex;

    track.style.transform = `translateX(-${currentIndex * 100}%)`;

    const prevButton = carousel.querySelector('.carousel-prev');
    const nextButton = carousel.querySelector('.carousel-next');
    prevButton.disabled = currentIndex === 0; // Corregido: currentPage a currentIndex
    nextButton.disabled = currentIndex === cards.length - 1;
}

// Inicializar la tabla y el conteo al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    updateTable();
    updateProductCount();
});