import cv2
import os

# ====== Change these paths ======
images_folder = r"C:\Users\22pa3\Downloads\images"
labels_folder = r"C:\Users\22pa3\Downloads\labels"
output_folder = r"C:\Users\22pa3\Downloads\output_images"

# Helmet class IDs
helmet_classes = {"1", "2", "3"}  # white helmet, yellow helmet, green helmet

# Ensure output directory exists BEFORE saving
os.makedirs(output_folder, exist_ok=True)

# Loop through all images in the images folder
for image_file in os.listdir(images_folder):
    if not image_file.lower().endswith(".jpg"):
        continue  # Skip non-image files

    image_path = os.path.join(images_folder, image_file)
    label_path = os.path.join(labels_folder, os.path.splitext(image_file)[0] + ".txt")
    output_path = os.path.join(output_folder, image_file)

    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ Image not found: {image_path}")
        continue

    h, w = img.shape[:2]

    # Check if label exists
    if not os.path.exists(label_path):
        print(f"⚠ Label file not found: {label_path}")
        continue

    with open(label_path, "r") as f:
        lines = f.readlines()

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    # Start with grey image and restore helmet areas
    output_img = gray_3ch.copy()

    for line in lines:
        cid, x_center, y_center, bbox_w, bbox_h = line.split()
        if cid in helmet_classes:
            x_center = float(x_center) * w
            y_center = float(y_center) * h
            bbox_w = float(bbox_w) * w
            bbox_h = float(bbox_h) * h

            x1 = max(0, int(x_center - bbox_w / 2))
            y1 = max(0, int(y_center - bbox_h / 2))
            x2 = min(w, int(x_center + bbox_w / 2))
            y2 = min(h, int(y_center + bbox_h / 2))

            # Restore helmet area in color
            output_img[y1:y2, x1:x2] = img[y1:y2, x1:x2]

    # Save the processed image
    if cv2.imwrite(output_path, output_img):
        print(f"✅ Saved: {output_path}")
    else:
        print(f"❌ Failed to save: {output_path}")

print("🎯 All images processed!")
