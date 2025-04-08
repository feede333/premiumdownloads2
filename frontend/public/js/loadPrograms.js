async function loadPrograms() {
    try {
        const response = await fetch('./data/programs.json');
        const data = await response.json();
        const programsGrid = document.getElementById('programsGrid');

        // Limpiar el contenedor
        programsGrid.innerHTML = '';

        // Agregar cada programa
        data.programs.forEach(program => {
            const programCard = createProgramCard(program);
            programsGrid.appendChild(programCard);
        });
    } catch (error) {
        console.error('Error cargando programas:', error);
        document.getElementById('programsGrid').innerHTML = 
            '<p class="error">Error cargando los programas. Por favor, intenta más tarde.</p>';
    }
}

function createProgramCard(program) {
    const card = document.createElement('div');
    card.className = 'program-card';
    
    card.innerHTML = `
        <a href="detail.html?id=${program.id}">
            <img src="${program.image}" alt="${program.title}">
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
    
    return card;
}

// Cargar programas cuando la página esté lista
document.addEventListener('DOMContentLoaded', loadPrograms);