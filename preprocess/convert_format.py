from PIL import Image, UnidentifiedImageError
import os

directory_path = './WeiXin'

all_files = os.listdir(directory_path)
image_files = [file for file in all_files if file.lower().endswith(('jpeg', 'jpg', 'png'))]

index = 1
for image_file in sorted(image_files):
    try:
        with Image.open(os.path.join(directory_path, image_file)) as img:
            exif_data = img.info.get("exif")
            output_path = os.path.join(directory_path, f"{index}.jpg")

            # Convert image to RGB before saving as JPEG
            rgb_image = img.convert('RGB')
            
            # Check if there is any exif data
            if exif_data:
                rgb_image.save(output_path, "JPEG", exif=exif_data)
            else:
                rgb_image.save(output_path, "JPEG")

            # Remove the original file only if it's different from the new file
            if os.path.abspath(image_file) != os.path.abspath(output_path):  
                os.remove(os.path.join(directory_path, image_file))
            
            index += 1  # Increment the index only after successful processing
    except UnidentifiedImageError:
        print(f"Cannot process image: {image_file}. Skipping.")