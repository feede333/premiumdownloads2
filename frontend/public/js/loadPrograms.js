async function loadPrograms() {
    try {
        const response = await fetch('./data/programs.json');
        if (!response.ok) {
            throw new Error('No se pudo cargar el archivo JSON');
        }
        const data = await response.json();
        const programsGrid = document.getElementById('programsGrid');

        data.programs.forEach(program => {
            const programCard = document.createElement('div');
            programCard.className = 'program-card';
            programCard.innerHTML = `
                <a href="detail.html?id=${program.id}">
                    <img src="${program.image}" alt="${program.title}">
                    <h3>${program.title}</h3>
                    <span class="category">${program.category}</span>
                    <div class="program-meta">
                        <span class="size">${program.fileSize}</span>
                        <span class="date">${program.date}</span>
                    </div>
                </a>
            `;
            programsGrid.appendChild(programCard);
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

// Cargar programas cuando el documento esté listo
document.addEventListener('DOMContentLoaded', loadPrograms);