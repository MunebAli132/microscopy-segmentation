import io

import numpy as np
import streamlit as st
from PIL import Image, UnidentifiedImageError
from skimage import color, filters, morphology, measure, segmentation


st.set_page_config(
    page_title="Microscopy Segmentation",
    page_icon="🔬",
    layout="wide",
)

st.title("🔬 Microscopy Image Segmentation")
st.caption(
    "A lightweight image-analysis app for threshold-based segmentation "
    "of microscopy images."
)

with st.sidebar:
    st.header("Segmentation settings")
    method = st.selectbox("Thresholding method", ["Otsu (automatic)", "Manual"])
    object_type = st.radio(
        "Objects of interest",
        ["Bright objects", "Dark objects"],
        help="Choose whether objects are brighter or darker than the background.",
    )
    manual_threshold = st.slider(
        "Manual threshold", 0.0, 1.0, 0.5, 0.01,
        disabled=(method != "Manual"),
    )
    min_size = st.slider("Remove objects smaller than (pixels)", 0, 10000, 50, 10)
    fill_holes = st.checkbox("Fill small holes", value=True)
    hole_size = st.slider(
        "Maximum hole size (pixels)", 0, 10000, 50, 10,
        disabled=not fill_holes,
    )
    show_boundaries = st.checkbox("Show object boundaries", value=True)

uploaded = st.file_uploader(
    "Upload a microscopy image",
    type=["png", "jpg", "jpeg", "tif", "tiff", "bmp"],
)

if uploaded is None:
    st.info("Upload an image to begin. Example images can be added to the `examples/` folder.")
    st.markdown(
        """
        **Workflow**
        1. Upload a brightfield, fluorescence, or other grayscale/RGB image.
        2. Choose bright or dark objects.
        3. Select automatic Otsu or manual thresholding.
        4. Adjust cleanup settings and inspect the mask and overlay.
        5. Download the binary mask and an overlay image.
        """
    )
    st.warning(
        "This is a classical threshold-based tool. It may not accurately separate "
        "touching cells, unevenly illuminated samples, or objects with low contrast."
    )
    st.stop()

try:
    pil_image = Image.open(uploaded)
    pil_image.load()
except (UnidentifiedImageError, OSError) as exc:
    st.error(f"Could not read this image: {exc}")
    st.stop()

image = np.asarray(pil_image.convert("RGB"))
gray = color.rgb2gray(image)

if method == "Otsu (automatic)":
    if np.allclose(gray.min(), gray.max()):
        st.error("The image has no intensity variation; thresholding cannot proceed.")
        st.stop()
    threshold = float(filters.threshold_otsu(gray))
else:
    threshold = float(manual_threshold)

if object_type == "Bright objects":
    mask = gray > threshold
else:
    mask = gray < threshold

if min_size > 0:
    mask = morphology.remove_small_objects(mask, min_size=min_size)

if fill_holes and hole_size > 0:
    mask = morphology.remove_small_holes(mask, area_threshold=hole_size)

# Label connected components for simple object counts and measurements.
labels = measure.label(mask, connectivity=2)
regions = measure.regionprops(labels)
object_count = len(regions)
foreground_pixels = int(mask.sum())
total_pixels = int(mask.size)
area_percent = 100.0 * foreground_pixels / total_pixels if total_pixels else 0.0

overlay = image.copy()
tint = np.zeros_like(overlay)
tint[..., 1] = 255
overlay[mask] = (
    0.55 * overlay[mask].astype(np.float32)
    + 0.45 * tint[mask].astype(np.float32)
).clip(0, 255).astype(np.uint8)

if show_boundaries and object_count:
    boundaries = segmentation.find_boundaries(labels, mode="outer")
    overlay[boundaries] = np.array([255, 40, 40], dtype=np.uint8)

st.subheader("Results")
left, middle, right = st.columns(3)
with left:
    st.image(image, caption="Original image", use_container_width=True)
with middle:
    st.image(mask.astype(np.uint8) * 255, caption="Binary mask", clamp=True, use_container_width=True)
with right:
    st.image(overlay, caption="Overlay (green = segmented, red = boundaries)", use_container_width=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Threshold", f"{threshold:.3f}")
m2.metric("Objects detected", f"{object_count:,}")
m3.metric("Foreground pixels", f"{foreground_pixels:,}")
m4.metric("Image area covered", f"{area_percent:.2f}%")

st.caption(
    "Object count is based on 8-connected components. Touching objects may be counted "
    "as one object unless they are separated by additional processing."
)

mask_image = Image.fromarray((mask.astype(np.uint8) * 255), mode="L")
overlay_image = Image.fromarray(overlay, mode="RGB")

mask_buffer = io.BytesIO()
mask_image.save(mask_buffer, format="PNG")
overlay_buffer = io.BytesIO()
overlay_image.save(overlay_buffer, format="PNG")

base_name = uploaded.name.rsplit(".", 1)[0]
d1, d2 = st.columns(2)
with d1:
    st.download_button(
        "⬇️ Download binary mask",
        data=mask_buffer.getvalue(),
        file_name=f"{base_name}_mask.png",
        mime="image/png",
        use_container_width=True,
    )
with d2:
    st.download_button(
        "⬇️ Download overlay",
        data=overlay_buffer.getvalue(),
        file_name=f"{base_name}_overlay.png",
        mime="image/png",
        use_container_width=True,
    )

with st.expander("About this result"):
    st.write(
        "The binary mask uses white pixels (255) for segmented foreground and "
        "black pixels (0) for background. Measurements are in pixels, not physical "
        "units. To obtain µm² or other calibrated units, image pixel size metadata "
        "or a user-supplied scale is required."
    )
