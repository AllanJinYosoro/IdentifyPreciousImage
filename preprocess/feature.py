import PIL.Image
import PIL.ExifTags
import csv
import os

def get_exif(image_path):
    img = PIL.Image.open(image_path)
    exif_data = img._getexif()

    if exif_data is None:
        return {}
    
    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in exif_data.items()
        if k in PIL.ExifTags.TAGS
    }
    return exif

def infer_image_properties(exif):
    apple_device = 0
    camera_shot = 0
    screenshot = 0

    # Check for Apple device
    if 'Make' in exif and exif['Make'] == 'Apple':
        apple_device = 1

    # Check for Apple Screenshot
    apple_screenshot_tags = ['ResolutionUnit', 'Orientation', 'ColorSpace', 'ExifImageWidth', 'ExifImageHeight']
    if apple_device and all(tag in exif for tag in apple_screenshot_tags) and 'DateTimeOriginal' not in exif:
        screenshot = 1

    # Check for Huawei Screenshot
    if 'Make' in exif and exif['Make'] == 'HUAWEI' and 'FocalLength' not in exif:
        screenshot = 1

    # Check for Camera shot
    camera_tags = [
    'ExposureTime', 'FNumber', 'ISOSpeedRatings', 'FocalLength',
    'DateTimeOriginal', 'Flash', 'MeteringMode', 'ExposureMode',
    'WhiteBalance', 'ExposureProgram', 'ShutterSpeedValue', 'ApertureValue'
]

    if any(tag in exif for tag in camera_tags):
        camera_shot = 1

    return apple_device, camera_shot, screenshot

# Specify your directory here
directory = "./photo"  # replace with your directory

# List of images in the directory with specific extensions
image_paths = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(('.jpg', '.png'))]

# Prepare the csv file
with open('image.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Image Name', 'Apple Device (1/0)', 'Camera Shot (1/0)', 'Screenshot (1/0)'])  # write header

    for path in image_paths:
        exif = get_exif(path)
        apple_device, camera_shot, screenshot = infer_image_properties(exif)
        csvwriter.writerow([os.path.basename(path), apple_device, camera_shot, screenshot])
