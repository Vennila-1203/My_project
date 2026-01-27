#PR Practice change
import os
import shutil

# -----------------------------
# User Config
# -----------------------------
dataset_path = "dataset"   # Path to full dataset
target_class_name = "pitted_surface"
folders = ["train", "valid", "test"]

output_folder = "pitted_surface_dataset"

os.makedirs(output_folder, exist_ok=False)

# -----------------------------
# Step 1: Get class ID
# -----------------------------
classes_file = os.path.join(dataset_path, "classes.txt")
with open(classes_file, "r") as f:
    classes = [line.strip() for line in f.readlines()]

if target_class_name not in classes:
    raise ValueError(f"{target_class_name} not found in classes.txt")

target_class_id = classes.index(target_class_name)
print(f"Class '{target_class_name}' has ID: {target_class_id}")

# -----------------------------
# Step 2: Filter dataset
# -----------------------------
for folder in folders:
    images_folder = os.path.join(dataset_path, folder, "images")
    labels_folder = os.path.join(dataset_path, folder, "labels")
    
    out_images_folder = os.path.join(output_folder, folder, "images")
    out_labels_folder = os.path.join(output_folder, folder, "labels")
    os.makedirs(out_images_folder, exist_ok=True)
    os.makedirs(out_labels_folder, exist_ok=True)
    
    label_files = os.listdir(labels_folder)
    count_kept = 0
    
    for label_file in label_files:
        label_path = os.path.join(labels_folder, label_file)
        with open(label_path, "r") as f:
            lines = f.readlines()
        
        # Keep only lines with target_class_id
        filtered_lines = [line for line in lines if int(line.split()[0]) == target_class_id]
        
        if len(filtered_lines) > 0:
            # Copy the annotation file
            with open(os.path.join(out_labels_folder, label_file), "w") as f:
                f.writelines(filtered_lines)
            
            # Copy corresponding image
            img_file_jpg = label_file.replace(".txt", ".jpg")
            img_file_png = label_file.replace(".txt", ".png")
            
            # Check which extension exists
            if os.path.exists(os.path.join(images_folder, img_file_jpg)):
                shutil.copy(os.path.join(images_folder, img_file_jpg), os.path.join(out_images_folder, img_file_jpg))
            elif os.path.exists(os.path.join(images_folder, img_file_png)):
                shutil.copy(os.path.join(images_folder, img_file_png), os.path.join(out_images_folder, img_file_png))
            
            count_kept += 1
    
    print(f"{folder}: Kept {count_kept} images with class '{target_class_name}'")

print("Filtered dataset ready in:", output_folder)
