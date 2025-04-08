async function loadPrograms() {
    try {
        // Cambia la ruta para GitHub Pages
        const response = await fetch('/premiumdownloads2/frontend/public/data/programs.json');
        if (!response.ok) {
            throw new Error('No se pudo cargar el archivo JSON');
        }
        const data = await response.json();
        const programsGrid = document.getElementById('programsGrid');

        data.programs.forEach(program => {
            const programCard = document.createElement('div');
            programCard.className = 'program-card';
            programCard.innerHTML = `
                <a href="/premiumdownloads2/frontend/public/detail.html?id=${program.id}">
                    <img src="/premiumdownloads2/${program.image}" alt="${program.title}">
                    <h3>${program.title}</h3>
                    <span class="category">${program.category}</span>
                    <div class="meta">
                        <span class="size">${program.fileSize}</span>
                        <span class="date">${program.date}</span>
                    </div>
                </a>
            `;
            programsGrid.appendChild(programCard);
        });
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('programsGrid').innerHTML = 
            '<p class="error">Error cargando los programas: ' + error.message + '</p>';
    }
}

// Cargar programas cuando la página esté lista
document.addEventListener('DOMContentLoaded', loadPrograms);