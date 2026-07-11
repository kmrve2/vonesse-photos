// Photo Gallery - Lightbox JavaScript
let currentImages = [];
let currentIndex = 0;

// Initialize full-size image list from data attribute
document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('photo-grid');
    if (grid) {
        try {
            currentImages = JSON.parse(grid.dataset.images || '[]');
        } catch(e) {
            console.error('Failed to parse image list:', e);
        }
    }
});

function openLightbox(index) {
    if (!currentImages.length) return;
    currentIndex = index;
    updateLightbox();
    document.getElementById('lightbox').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    document.getElementById('lightbox').classList.remove('active');
    document.body.style.overflow = '';
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
    
    // Log for debugging
    console.log('Loading image:', currentImages[currentIndex]);
}

// Keyboard navigation
document.addEventListener('keydown', function(e) {
    const lightbox = document.getElementById('lightbox');
    if (!lightbox || !lightbox.classList.contains('active')) return;
    
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

// Close lightbox when clicking outside image
document.addEventListener('click', function(e) {
    const lightbox = document.getElementById('lightbox');
    if (lightbox && e.target === lightbox) {
        closeLightbox();
    }
});