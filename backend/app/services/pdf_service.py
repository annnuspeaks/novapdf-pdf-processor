from io import BytesIO

from PIL import Image, UnidentifiedImageError


def images_to_pdf(image_contents: list[bytes]) -> bytes:
    """Convert supported images into a single PDF in memory."""

    if not image_contents:
        raise ValueError("Upload at least one image.")

    pdf_images = []

    try:
        for content in image_contents:
            with Image.open(BytesIO(content)) as source:
                if source.format not in {"JPEG", "PNG"}:
                    raise ValueError(
                        "Only genuine JPEG and PNG images are supported."
                    )

                source.load()

                # PDF pages use RGB or grayscale, not RGBA/palette modes.
                if source.mode in {"RGBA", "LA", "P"}:
                    rgba = source.convert("RGBA")
                    background = Image.new("RGB", rgba.size, "white")
                    background.paste(rgba, mask=rgba.getchannel("A"))
                    converted = background
                else:
                    converted = source.convert("RGB")

                pdf_images.append(converted.copy())

    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("One or more uploaded images are invalid.") from exc

    if not pdf_images:
        raise ValueError("No valid images were provided.")

    output = BytesIO()

    try:
        pdf_images[0].save(
            output,
            format="PDF",
            save_all=True,
            append_images=pdf_images[1:],
            resolution=150.0,
        )
        return output.getvalue()
    finally:
        for image in pdf_images:
            image.close()