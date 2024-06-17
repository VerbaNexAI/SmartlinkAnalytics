
        let cropper;

        document.getElementById('uploadButton').addEventListener('click', async () => {
            const input = document.getElementById('inputImage');
            if (input.files.length > 0) {
                const formData = new FormData();
                formData.append('file', input.files[0]);

                const response = await fetch('http://127.0.0.1:8000/upload-image/', {
                    method: 'POST',
                    body: formData,
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const url = URL.createObjectURL(blob);
                    document.getElementById('uploadedImage').src = url;

                    // Destroy existing cropper instance if it exists
                    if (cropper) {
                        cropper.destroy();
                    }

                    // Initialize Cropper.js
                    const image = document.getElementById('uploadedImage');
                    cropper = new Cropper(image, {
                        aspectRatio: 16 / 9,
                        viewMode: 1,
                        preview: '.img-preview',
                        ready() {
                            const data = cropper.getData();
                            document.getElementById('dataX').value = Math.round(data.x);
                            document.getElementById('dataY').value = Math.round(data.y);
                            document.getElementById('dataWidth').value = Math.round(data.width);
                            document.getElementById('dataHeight').value = Math.round(data.height);
                            document.getElementById('dataRotate').value = Math.round(data.rotate);
                            document.getElementById('dataScaleX').value = data.scaleX;
                            document.getElementById('dataScaleY').value = data.scaleY;
                        },
                        crop(event) {
                            document.getElementById('dataX').value = Math.round(event.detail.x);
                            document.getElementById('dataY').value = Math.round(event.detail.y);
                            document.getElementById('dataWidth').value = Math.round(event.detail.width);
                            document.getElementById('dataHeight').value = Math.round(event.detail.height);
                            document.getElementById('dataRotate').value = Math.round(event.detail.rotate);
                            document.getElementById('dataScaleX').value = event.detail.scaleX;
                            document.getElementById('dataScaleY').value = event.detail.scaleY;
                        }
                    });
                } else {
                    console.error('Error uploading image');
                }
            }
        });