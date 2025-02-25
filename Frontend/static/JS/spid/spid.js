import { initializeImageGallery } from '../imageGalleryModule.js';

document.addEventListener('DOMContentLoaded', () => {
    const url = 'http://127.0.0.1:8000/upload-image-spid';
    const herramienta = 'Smart PID';
    initializeImageGallery(url, herramienta);
});
