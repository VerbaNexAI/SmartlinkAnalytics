
            for i, result in enumerate(predictions):
                # Access the boxes attribute to get detected objects
                detections = []
                for box in result.boxes:
                    # Convert the confidence score tensor to a float
                    conf = box.conf.item()
                    # Convert confidence to percentage and round it
                    conf_percentage = round(conf * 100, 2)
                    print(f"Confianza: {conf_percentage}%")
                    detections.append({
                        "class": int(box.cls.item()),  # Ensure class is an int
                        "confidence": conf_percentage
                    })

                # Plot results image
                im_bgr = result.plot(font_size=1.2)  # BGR-order numpy array

                # Save processed image
                processed_image_path = os.path.join(processed_folder, f"{os.path.splitext(file.filename)[0]}_result_{i}.jpg")