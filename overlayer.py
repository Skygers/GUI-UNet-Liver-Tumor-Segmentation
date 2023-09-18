from PIL import Image
import cv2
import numpy as np

# Load the CT scan image (JPEG)
ct_scan = Image.open("img/volume-0_slice_60.jpg")

# Load the segmentation mask (TIFF)
segmentation_mask = cv2.imread("img/volume-0_slice_60.tiff", cv2.IMREAD_GRAYSCALE)
# Resize segmentation mask to match the CT scan image size
segmentation_mask = cv2.resize(segmentation_mask, (ct_scan.width, ct_scan.height))
# Define the transparency level (adjust as needed)
ct_scan = np.array(ct_scan)
alpha = 0.5

# Create an overlay by blending the images
overlay = cv2.addWeighted(ct_scan, 1 - alpha, segmentation_mask, alpha, 0)
cv2.imshow("Overlay", overlay)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("overlay_result.jpg", overlay)
