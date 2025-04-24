import { initializeImageGallery } from '../imageGalleryModule.js';

document.addEventListener('DOMContentLoaded', () => {
    const url = 'http://192.168.0.226:5200/upload-image-firmas';
    const herramienta = 'Firmas';
    initializeImageGallery(url, herramienta);
});
