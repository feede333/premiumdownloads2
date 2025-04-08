async function loadPrograms() {
    try {
        console.log('Intentando cargar programas...');
        // Ruta absoluta para GitHub Pages
        const response = await fetch('/premiumdownloads2/data/programs.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Datos cargados:', data);

        const programsGrid = document.getElementById('programsGrid');
        if (!programsGrid) {
            throw new Error('No se encontró el elemento programsGrid');
        }

        // Limpiar el grid
        programsGrid.innerHTML = '';

        data.programs.forEach(program => {
            const programCard = document.createElement('div');
            programCard.className = 'program-card';
            
            // Usar rutas absolutas para GitHub Pages
            const imagePath = program.image.startsWith('/') ? program.image : `/premiumdownloads2/${program.image}`;
            
            programCard.innerHTML = `
                <a href="/premiumdownloads2/detail.html?id=${program.id}">
                    <img src="${imagePath}" alt="${program.title}">
                    <div class="program-info">
                        <h3>${program.title}</h3>
                        <span class="category">${program.category}</span>
                        <div class="meta">
                            <span class="size">${program.fileSize}</span>
                            <span class="date">${program.date}</span>
                        </div>
                    </div>
                </a>
            `;
            programsGrid.appendChild(programCard);
        });
    } catch (error) {
        console.error('Error cargando programas:', error);
        const programsGrid = document.getElementById('programsGrid');
        if (programsGrid) {
            programsGrid.innerHTML = `<p class="error">Error cargando programas: ${error.message}</p>`;
        }
    }
}

// Cargar programas cuando el documento esté listo
document.addEventListener('DOMContentLoaded', loadPrograms);