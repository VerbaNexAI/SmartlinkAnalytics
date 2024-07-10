import { initializeImageGallery } from '../imageGalleryModule.js';

document.addEventListener('DOMContentLoaded', () => {
    const url = 'http://192.168.0.226:5200/upload-image-s3d-electrica';
    const herramienta = 'Electrica';
    initializeImageGallery(url, herramienta);
});
