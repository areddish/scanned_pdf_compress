import fitz
from PIL import Image
import io
import os

def size_str(size):
    if size < 1024:
        return f"{size} bytes"
    elif size < 1024*1024:
        return f"{size//1024} KB"
    elif size < 1024*1024*1024:
        return f"{size//(1024*1024)} MB"
    return f"{size//(1024*1024*1024)} GB"

INPUT = input("Enter file name or hit enter to default to [input.pdf]:") or "input.pdf"
if not os.path.exists(INPUT):
    print("Error: "+INPUT+" doesn't exist.")
    exit(-1)

OUTPUT = INPUT[:-4]+"_compressed.pdf"
if os.path.exists(OUTPUT):
    print("Error: "+OUTPUT+" already exists.")
    overwrite = input("Overwrite (Y/N)?").lower()
    if overwrite != "y":
       exit(0)

JPEG_QUALITY = 60

input_size = os.path.getsize(INPUT)
print("Processing ["+INPUT+"] with original size of",size_str(input_size))

doc = fitz.open(INPUT)

for page in doc:
    images = page.get_images(full=True)

    for img in images:
        xref = img[0]

        base = doc.extract_image(xref)
        img_bytes = base["image"]

        try:
            pil = Image.open(io.BytesIO(img_bytes))
        except:
            continue

        # Convert safely
        if pil.mode not in ("RGB", "L"):
            pil = pil.convert("RGB")

        # Recompress
        buf = io.BytesIO()
        pil.save(buf, format="JPEG", quality=JPEG_QUALITY, optimize=True)
        new_bytes = buf.getvalue()

        # Find where this image is drawn
        rects = page.get_image_rects(xref)

        for r in rects:
            # Cover old image
            page.add_redact_annot(r, fill=(1, 1, 1))
        page.apply_redactions()

        # Reinsert new image at same position
        for r in rects:
            page.insert_image(r, stream=new_bytes)

doc.save(OUTPUT, garbage=4, deflate=True)
doc.close()

output_size = os.path.getsize(OUTPUT)
print("Saved:", OUTPUT, "with new size of", size_str(output_size), "which is", f"{100*abs(output_size-input_size)/input_size:.2f}","% smaller")
