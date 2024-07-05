document.addEventListener('DOMContentLoaded', () => {
    
    const imageGallery = document.getElementById('image-gallery');
    const fileInput = document.getElementById('file-input');
    const gallery = document.getElementById('gallery');
    const fileSelect = document.getElementById('file-select');
    const sendButton = document.getElementById('send-button');
    const container = document.getElementById('container');
    const galleryContainer = document.getElementById('gallery-container');
    const addMoreImagesBtn = document.getElementById('add-more-images-btn');
    const downloadCurrentImageBtn = document.getElementById('download-current-image-btn');
    const downloadPdfButton = document.getElementById('download-pdf-button');

    const galleryResponseContainer = document.getElementById('gallery-response-container');
    const mainImageResponse = document.getElementById('main-image_response');
    const thumbnailsResponse = document.getElementById('thumbnails_response');

    // Array para mantener registros de todas las imágenes seleccionadas
    let allSelectedImages = [];
    let processedImages = []; // Definir la variable processedImages

    // Manejo de clics en la galería de imágenes y el selector de archivos
    fileSelect.addEventListener('click', () => fileInput.click());
    imageGallery.addEventListener('click', () => fileInput.click());

    // Manejo de arrastrar y soltar archivos en la galería de imágenes
    imageGallery.addEventListener('dragover', (event) => {
        event.preventDefault();
        imageGallery.classList.add('dragover');
    });
    imageGallery.addEventListener('dragleave', () => imageGallery.classList.remove('dragover'));
    imageGallery.addEventListener('drop', (event) => {
        event.preventDefault();
        imageGallery.classList.remove('dragover');
        handleFiles(event.dataTransfer.files);
    });

    // Manejo de cambios en el input de archivos
    fileInput.addEventListener('change', (event) => handleFiles(event.target.files));

    // Envío de imágenes al hacer clic en el botón de enviar
    sendButton.addEventListener('click', async (event) => {
        event.preventDefault();

        // Obtener imágenes únicas seleccionadas
        const uniqueImages = Array.from(new Set(allSelectedImages.map(image => image.name)));
        const formData = new FormData();

        uniqueImages.forEach(imageName => {
            const image = allSelectedImages.find(img => img.name === imageName);
            formData.append('files', image);
        });

        try {
            const response = await fetch('http://127.0.0.1:8000/upload-image-s3d-mecanica', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                console.log('Files uploaded successfully');
                processedImages = await response.json(); // Asignar a processedImages
                displayProcessedImages(processedImages);
                alert('Imágenes enviadas y procesadas correctamente.');
            } else {
                console.error('Failed to upload files');
                alert('Hubo un problema al enviar las imágenes.');
            }
        } catch (error) {
            console.error('Error uploading files', error);
            alert('Error al enviar las imágenes:', error);
        }
    });

    // Función para mostrar las imágenes procesadas
    function displayProcessedImages(images) {
        thumbnailsResponse.innerHTML = ''; // Limpiar miniaturas existentes

        images.forEach(imageData => {
            const img = document.createElement('img');
            img.src = `data:image/jpeg;base64, ${imageData.image_base64}`;
            img.alt = 'Imagen procesada';
            img.className = 'thumbnail';
            img.onclick = () => changeImage(img.src);

            const thumbnailItem = document.createElement('div');
            thumbnailItem.className = 'thumbnail-item';
            thumbnailItem.appendChild(img);

            thumbnailsResponse.appendChild(thumbnailItem);

            // Agregar imagen grande
            if (!mainImageResponse.src || mainImageResponse.src === 'https://via.placeholder.com/800x600') {
                mainImageResponse.src = img.src;
            }
        });

        // Ocultar la sesión anterior y mostrar la nueva
        container.classList.add('none');
        galleryContainer.classList.add('none');
        galleryResponseContainer.classList.remove('none');
    }

    // Función para cambiar la imagen principal
    function changeImage(imageSrc) {
        mainImageResponse.src = imageSrc;
    }

    // Agregar más imágenes al hacer clic en el botón correspondiente
    addMoreImagesBtn.addEventListener('click', () => fileInput.click());

    // Manejo de descarga de la imagen visible
    downloadCurrentImageBtn.addEventListener('click', () => {
        const link = document.createElement('a');
        link.href = mainImageResponse.src;
        link.download = 'imagen_descargada.jpg';
        link.click();
    });

    downloadPdfButton.addEventListener('click', async () => {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
    
        // Título del reporte en la primera página
        doc.setFontSize(20);
        doc.text('REPORTE DE VALIDACIÓN DE CONSISTENCIA', 20, 20);

        // Recorrer todas las imágenes procesadas
        for (let i = 0; i < processedImages.length; i++) {
            const imageData = processedImages[i];
            const base64Img = `data:image/jpeg;base64,${imageData.image_base64}`;
    
            console.log(imageData);
            console.log(imageData.filename);
    
            // Obtener los datos asociados a la imagen desde dataset de miniatura
            const fechaGeneracion = imageData['Fecha de Generación'];
            const empresa = imageData['Empresa'];
            const detecciones = imageData['Detecciones'];
    
            const imageFileName = imageData.filename;
            const tableData = detecciones
                .filter(deteccion => deteccion.Imagen === imageFileName)
                .map(deteccion => [
                    deteccion.Clase,
                    deteccion.Confianza.toFixed(3),
                    deteccion.Box_X1.toFixed(3),
                    deteccion.Box_Y1.toFixed(3),
                    deteccion.Box_X2.toFixed(3),
                    deteccion.Box_Y2.toFixed(3)
                ]);
    
            // Asegurarse de que haya espacio suficiente para la tabla
            if (i > 0) {
                doc.addPage();
            }

            // Agregar la información al principio del PDF
            doc.autoTable({
                startY: 30,
                head: [['Fecha de Generación', 'Herramienta', 'Empresa', 'Nombre de la imagen']],
                body: [
                    [fechaGeneracion, 'Mecanica', empresa, imageData.filename]
                ]
            });
    
            // Agregar la imagen al PDF
            doc.addImage(base64Img, 'JPEG', 20, 60, 160, 120);
    
            // Calcular la posición Y de la segunda tabla
            const imageHeight = 120; // Altura de la imagen
            const imageStartY = 60; // Coordenada Y de inicio de la imagen
            const tableStartY = imageStartY + imageHeight + 10; // Espacio adicional entre la imagen y la tabla
    
            // Agregar la tabla de detecciones al PDF
            doc.autoTable({
                startY: tableStartY,
                head: [['Clase', 'Confianza', 'Box_X1', 'Box_Y1', 'Box_X2', 'Box_Y2']],
                body: tableData,
            });
        }
    
        // Descargar el PDF
        doc.save('REPORTE DE VALIDACIÓN DE CONSISTENCIA.pdf');
    });  

    // Manejo de archivos seleccionados
    function handleFiles(files) {
        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            const reader = new FileReader();
            reader.onload = (event) => {
                const imgContainer = document.createElement('div');
                imgContainer.className = 'img-container';

                const img = document.createElement('img');
                img.src = event.target.result;

                const deleteIcon = document.createElement('i');
                deleteIcon.className = 'fas fa-times-circle delete-icon';
                deleteIcon.addEventListener('click', () => {
                    imgContainer.remove();
                    updateImageSizes();
                });

                imgContainer.appendChild(img);
                imgContainer.appendChild(deleteIcon);
                gallery.appendChild(imgContainer);
                updateImageSizes();
            }
            reader.readAsDataURL(file);
            allSelectedImages.push(file); // Agregar archivo al registro
        }
        container.classList.add('none');
        galleryContainer.classList.remove('none');
    }

    // Actualización de tamaños de imagen según la cantidad
    function updateImageSizes() {
        const images = gallery.querySelectorAll('.img-container');
        images.forEach(image => {
            image.classList.remove('large', 'medium');
            if (images.length >= 1 && images.length <= 4) {
                image.classList.add('large');
            } else if (images.length > 4) {
                image.classList.add('medium');
            }
        });
    }
});
