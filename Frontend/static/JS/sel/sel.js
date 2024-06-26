document.addEventListener('DOMContentLoaded', function() {
    var uploadedImageURL;
    var cropper;
    var selectedFile;

    document.getElementById('inputImage').addEventListener('change', function() {
        selectedFile = this.files[0];
    });

    document.getElementById('downloadBtn').addEventListener('click', function() {
        if (!cropper) {
            return;
        }

        var croppedCanvas = cropper.getCroppedCanvas();
        if (!croppedCanvas) {
            alert('No se pudo obtener la imagen recortada. Asegúrate de recortar la imagen antes de descargarla.');
            return;
        }

        croppedCanvas.toBlob(function(blob) {
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'cropped.jpg';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        });
    });

    document.getElementById('submitBtn').addEventListener('click', function() {
        if (!selectedFile) {
            alert('No hay imagen seleccionada para enviar.');
            return;
        }

        var formData = new FormData();
        formData.append('file', selectedFile);

        fetch('http://127.0.0.1:8000/upload-image', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.blob();
        })
        .then(blob => {
            var imageUrl = URL.createObjectURL(blob);
            uploadedImageURL = imageUrl;

            var uploadedImage = document.getElementById('uploadedImage');
            if (!uploadedImage) {
                throw new Error("Elemento #uploadedImage no encontrado.");
            }
            uploadedImage.src = imageUrl;
            uploadedImage.style.display = 'block'; // Mostrar la imagen

            $('#imageModal').modal('show');

            $('#imageModal').on('shown.bs.modal', function () {
                if (cropper) {
                    cropper.destroy(); 
                }

                cropper = new Cropper(uploadedImage, {
                    viewMode: 1, 
                    responsive: true,
                    zoomOnWheel: true,
                    cropBoxResizable: true, 
                    toggleDragModeOnDblclick: false,
                    movable: true, 
                    zoomable: true, 
                    rotatable: true, 
                    autoCropArea: 0.5, 
                    crop: function(event) {
                        var data = event.detail;
                        console.log(data);
                    }
                });
            });

            $('#imageModal').on('hidden.bs.modal', function () {
                if (cropper) {
                    cropper.destroy();
                    cropper = null;
                }
            });

            alert('Imagen cargada correctamente');
        })
        .catch(error => {
            console.error('Hubo un problema al enviar la imagen:', error);
            alert('Hubo un problema al enviar la imagen.');
        });
    });
});