// Vonesse Photos - Gallery JavaScript
let currentImages = [];
let currentIndex = 0;

// Sample album structure - this will be populated by generate-gallery.py
const albums = [
    {
        name: "Działka",
        description: "Family cottage and garden",
        cover: "photos/dzialka/cover.jpg",
        photos: []
    },
    {
        name: "Pets", 
        description: "Doodle, Beans, Figaro, and Macchiato",
        cover: "photos/pets/cover.jpg",
        photos: []
    },
    {
        name: "Projects",
        description: "Builds and creations",
        cover: "photos/projects/cover.jpg", 
        photos: []
    }
];

// Initialize gallery on page load
document.addEventListener('DOMContentLoaded', function() {
    loadGallery();
});

function loadGallery() {
    const gallery = document.getElementById('gallery');
    gallery.innerHTML = '';
    
    albums.forEach((album, index) => {
        const card = document.createElement('div');
        card.className = 'album-card';
        card.onclick = () => openAlbum(index);
        
        card.innerHTML = `
            <div class="album-cover" style="background: linear-gradient(135deg, #374151, #1f2937); height: 250px; display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 3rem;">📸</span>
            </div>
            <div class="album-info">
                <h3 class="album-title">${album.name}</h3>
                <p class="album-count">${album.description}</p>
            </div>
        `;
        
        gallery.appendChild(card);
    });
}

function openAlbum(albumIndex) {
    const album = albums[albumIndex];
    // For now, just show a message - will be enhanced with photo loading
    alert(`Opening ${album.name}...`);
}

// Lightbox functions
function openLightbox(images, index) {
    currentImages = images;
    currentIndex = index;
    updateLightbox();
    document.getElementById('lightbox').classList.add('active');
}

function closeLightbox() {
    document.getElementById('lightbox').classList.remove('active');
}

function prevImage() {
    currentIndex = (currentIndex - 1 + currentImages.length) % currentImages.length;
    updateLightbox();
}

function nextImage() {
    currentIndex = (currentIndex + 1) % currentImages.length;
    updateLightbox();
}

function updateLightbox() {
    const img = document.getElementById('lightbox-img');
    const caption = document.getElementById('lightbox-caption');
    
    img.src = currentImages[currentIndex];
    caption.textContent = `${currentIndex + 1} / ${currentImages.length}`;
}

// Keyboard navigation
document.addEventListener('keydown', function(e) {
    if (!document.getElementById('lightbox').classList.contains('active')) return;
    
    switch(e.key) {
        case 'Escape':
            closeLightbox();
            break;
        case 'ArrowLeft':
            prevImage();
            break;
        case 'ArrowRight':
            nextImage();
            break;
    }
});