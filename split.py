import os
import shutil

# ====== Change this path to your folder containing both jpg and txt files ======
source_folder = r"C:\Users\22pa3\Downloads\roller\obj_train_data"

# Create destination folders
images_folder = os.path.join(source_folder, "images")
labels_folder = os.path.join(source_folder, "labels")

os.makedirs(images_folder, exist_ok=True)
os.makedirs(labels_folder, exist_ok=True)

# Loop through all files in the source folder
for file_name in os.listdir(source_folder):
    file_path = os.path.join(source_folder, file_name)

    # Skip directories
    if os.path.isdir(file_path):
        continue

    # Move JPG files
    if file_name.lower().endswith(".jpg"):
        shutil.move(file_path, os.path.join(images_folder, file_name))

    # Move TXT files
    elif file_name.lower().endswith(".txt"):
        shutil.move(file_path, os.path.join(labels_folder, file_name))

print("✅ Files separated into:")
print(f"   Images -> {images_folder}")
print(f"   Labels -> {labels_folder}")
