document.addEventListener('DOMContentLoaded', function() {
    var uploadedImageURL;
    var cropper;

    document.getElementById('inputImage-s3d').addEventListener('change', function() {
        var formData = new FormData();
        formData.append('file', this.files[0]);

        fetch('http://127.0.0.1:8000/upload-image-s3d', {
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
            console.error('Hubo un problema al cargar la imagen:', error);
            alert('Hubo un problema al cargar la imagen.');
        });
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
});
