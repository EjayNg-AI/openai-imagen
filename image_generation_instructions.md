OpenAI has released an Image Generation API. I have provided full details together with worked examples below.

This model and its release notes are dated after your training cut off date, all this will be new to you. Do _NOT_ attempt to search online for instructions on how to use the Image API. I have carefully curated all the necessary information and provided them to you in a readable format.

Our task is to build a full stack web app to make use of the Image API, taking advantage of all its features.

First, I will need you to review the instructions and examples attached below, provide a high level summary, and analyze how we can build a full stack app.

## Overview

The OpenAI Image API lets you generate and edit images from text prompts, using the latest and most advanced model for image generation, `gpt-image-1`, a natively multimodal language model.

I will use the Image API with the following endpoints, each with distinct capabilities:

- Generations: Generate images from scratch based on a text prompt

- Edits: Modify existing images using a new prompt, either partially or entirely

You can also customize the output by specifying the quality, size, format, compression, and whether you would like a transparent background.

## Generate Images

You can use the image generation endpoint to create images based on text prompts. You can set the `n` parameter to generate multiple images at once in a single request (by default, the API returns a single image).

The following is example Python code for generating an image:

```python

# Generate an image

from openai import OpenAI
import base64
client = OpenAI()

prompt = """
A children's book drawing of a veterinarian using a stethoscope to
listen to the heartbeat of a baby otter.
"""

result = client.images.generate(
    model="gpt-image-1",
    prompt=prompt
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

# Save the image to a file
with open("otter.png", "wb") as f:
    f.write(image_bytes)

```

## Editing Images

The image edits endpoint lets you:

- Edit existing images

- Generate new images using other images as a reference

- Edit parts of an image by uploading an image and mask indicating which areas should be replaced (a process known as inpainting)

### Create a new image using image references

You can use one or more images as a reference to generate a new image.

In this example, we use 4 input images to generate a new image of a gift basket containing the items in the reference images.

```python

# Create a new image using image references

import base64
from openai import OpenAI
client = OpenAI()

prompt = """
Generate a photorealistic image of a gift basket on a white background
labeled 'Relax & Unwind' with a ribbon and handwriting-like font,
containing all the items in the reference pictures.
"""

result = client.images.edit(
    model="gpt-image-1",
    image=[
        open("body-lotion.png", "rb"),
        open("bath-bomb.png", "rb"),
        open("incense-kit.png", "rb"),
        open("soap.png", "rb"),
    ],
    prompt=prompt
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

# Save the image to a file
with open("gift-basket.png", "wb") as f:
    f.write(image_bytes)

```

### Editing an image using a mask (inpainting)

You can provide a mask to indicate where the image should be edited. The transparent areas of the mask will be replaced, while the black areas will be left unchanged.

You can use the prompt to describe the full new image, not just the erased area. If you provide multiple input images, the mask will be applied to the first image.

```python

# Edit an image using a mask (inpainting)

from openai import OpenAI
client = OpenAI()

result = client.images.edit(
    model="gpt-image-1",
    image=open("sunlit_lounge.png", "rb"),
    mask=open("mask.png", "rb"),
    prompt="A sunlit indoor lounge area with a pool containing a flamingo"
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

# Save the image to a file
with open("composition.png", "wb") as f:
    f.write(image_bytes)

```

Mask requirements:

- The image to edit and mask must be of the same format and size (less than 25MB in size).

- The mask image must also contain an alpha channel. If you're using an image editing tool to create the mask, make sure to save the mask with an alpha channel.

You can modify a black and white image programmatically to add an alpha channel:

```python

# Add an alpha channel to a black and white mask

from PIL import Image
from io import BytesIO

# 1. Load your black & white mask as a grayscale image
mask = Image.open(img_path_mask).convert("L")

# 2. Convert it to RGBA so it has space for an alpha channel
mask_rgba = mask.convert("RGBA")

# 3. Then use the mask itself to fill that alpha channel
mask_rgba.putalpha(mask)

# 4. Convert the mask into bytes
buf = BytesIO()
mask_rgba.save(buf, format="PNG")
mask_bytes = buf.getvalue()

# 5. Save the resulting file
img_path_mask_alpha = "mask_alpha.png"
with open(img_path_mask_alpha, "wb") as f:
    f.write(mask_bytes)

```

## Customize Image Output

You can configure the following output options:

- Size: Image dimensions (e.g., `1024x1024`, `1024x1536`)

- Quality: Rendering quality (e.g. `low`, `medium`, `high`)

- Format: File output format

- Compression: Compression level (0-100%) for JPEG and WebP formats

- Background: Transparent or opaque

## Size and quality options

Square images with standard quality are the fastest to generate. The default size is `1024x1024` pixels.

Available sizes:

- `1024x1024` (square)
- `1536x1024` (portrait)
- `1024x1536` (landscape)
- `auto` (default)

Quality options:

- `low`
- `medium`
- `high`
- `auto` (default)

## Output format

The Image API returns base64-encoded image data. The default format is `png`, but you can also request `jpeg` or `webp`.

If using `jpeg` or `webp`, you can also specify the output_compression parameter to control the compression level (0-100%). For example, `output_compression=50` will compress the image by 50%.

## Transparency

The `gpt-image-1` model supports transparent backgrounds. To enable transparency, set the `background` parameter to `transparent`.

It is only supported with the `png` and `webp` output formats.

Transparency works best when setting the quality to `medium` or `high`.

```python

# Generate an image with a transparent background

from openai import OpenAI
import base64
client = OpenAI()

result = client.images.generate(
    model="gpt-image-1",
    prompt="Draw a 2D pixel art style sprite sheet of a tabby gray cat",
    size="1024x1024",
    background="transparent",
    quality="high",
)

image_base64 = result.json()["data"][0]["b64_json"]
image_bytes = base64.b64decode(image_base64)

# Save the image to a file
with open("sprite.png", "wb") as f:
    f.write(image_bytes)

```

## Content Moderation

All prompts and generated images are filtered in accordance with our content policy.

For image generation using `gpt-image-1`, you can control moderation strictness with the `moderation` parameter. This parameter supports two values:

- `auto` (default): Standard filtering that seeks to limit creating certain categories of potentially age-inappropriate content.

- `low`: Less restrictive filtering.

## Examples

In this section, we provide examples of how to use `gpt-image-1`.

### Set Up

```bash
pip install pillow openai
```

```python

import base64
import os
from openai import OpenAI
from PIL import Image
from io import BytesIO
from IPython.display import Image as IPImage, display

client = OpenAI()
# Set your API key if not set globally
#client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))

# Create imgs/ folder
folder_path = "imgs"
os.makedirs(folder_path, exist_ok=True)

```

### Generate an image

`gpt-image-1`is great at instruction-following, meaning you can prompt the model to generate images with very detailed instructions.

```python

prompt1 = """
Render a realistic image of this character:
Blobby Alien Character Spec Name: Glorptak (or nickname: "Glorp")
Visual Appearance Body Shape: Amorphous and gelatinous. Overall silhouette resembles a teardrop or melting marshmallow, shifting slightly over time. Can squish and elongate when emotional or startled.
Material Texture: Semi-translucent, bio-luminescent goo with a jelly-like wobble. Surface occasionally ripples when communicating or moving quickly.
Color Palette:
- Base: Iridescent lavender or seafoam green
- Accents: Subsurface glowing veins of neon pink, electric blue, or golden yellow
- Mood-based color shifts (anger = dark red, joy = bright aqua, fear = pale gray)
Facial Features:
- Eyes: 3–5 asymmetrical floating orbs inside the blob that rotate or blink independently
- Mouth: Optional—appears as a rippling crescent on the surface when speaking or emoting
- No visible nose or ears; uses vibration-sensitive receptors embedded in goo
- Limbs: None by default, but can extrude pseudopods (tentacle-like limbs) when needed for interaction or locomotion. Can manifest temporary feet or hands.
Movement & Behavior Locomotion:
- Slides, bounces, and rolls.
- Can stick to walls and ceilings via suction. When scared, may flatten and ooze away quickly.
Mannerisms:
- Constant wiggling or wobbling even at rest
- Leaves harmless glowing slime trails
- Tends to absorb nearby small objects temporarily out of curiosity
"""

img_path1 = "imgs/glorptak.jpg"

# Generate the image
result1 = client.images.generate(
    model="gpt-image-1",
    prompt=prompt1,
    size="1024x1024"
)

# Save the image to a file and resize/compress for smaller files
image_base64 = result1.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

image = Image.open(BytesIO(image_bytes))
image = image.resize((300, 300), Image.LANCZOS)
image.save(img_path1, format="JPEG", quality=80, optimize=True)

# Show the result
display(IPImage(img_path1))

```

### Customize the output

You can customize the following output properties:

- Quality can be `low`, `medium`, `high` or `auto` (default value)

- Size can be `1024x1024` (square), `1536x1024` (portrait), `1024x1536` (landscape) or `auto` (default)

You can adjust the `output_compression` (from 0-100) for JPEG and WEBP formats

You can choose to generate an image with a transparent background (only available for PNG or WEBP)

```python

prompt2 = "generate a portrait, pixel-art style, of a grey tabby cat dressed as a blond woman on a dark background."
img_path2 = "imgs/cat_portrait_pixel.jpg"

# Generate the image
result2 = client.images.generate(
    model="gpt-image-1",
    prompt=prompt2,
    quality="low",
    output_compression=50,
    output_format="jpeg",
    size="1024x1536"
)

# Save the image to a file and resize/compress for smaller files
image_base64 = result2.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

image = Image.open(BytesIO(image_bytes))
image = image.resize((250, 375), Image.LANCZOS)
image.save(img_path2, format="JPEG", quality=80, optimize=True)

# Show the result
display(IPImage(img_path2))

```

### Transparent background

You can use the `background` property to request a transparent background, but if you include in your prompt that you want a transparent background, it will be set to `transparent` by default.

```python

prompt3 = "generate a pixel-art style picture of a green bucket hat with a pink quill on a transparent background."
img_path3 = "imgs/hat.png"

result3 = client.images.generate(
    model="gpt-image-1",
    prompt=prompt3,
    quality="low",
    output_format="png",
    size="1024x1024"
)
image_base64 = result3.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

# Save the image to a file and resize/compress for smaller files
image_base64 = result3.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

image = Image.open(BytesIO(image_bytes))
image = image.resize((250, 250), Image.LANCZOS)
image.save(img_path3, format="PNG")

# Show the result
display(IPImage(img_path3))

```

### Edit images

`gpt-image-1` can also accept image inputs, and use them to create new images. You can also provide a mask if you don't want the model to change a specific part of the input image.

You can use a maximum of 10 input images, and if you use a mask, it will be applied to the first image provided in the `image` array.

```python

prompt_edit = """
Combine the images of the cat and the hat to show the cat wearing the hat while being perched in a tree, still in pixel-art style.
"""
img_path_edit = "imgs/cat_with_hat.jpg"

img1 = open(img_path2, "rb")
img2 = open(img_path3, "rb")

# Generate the new image
result_edit = client.images.edit(
    model="gpt-image-1",
    image=[img1,img2],
    prompt=prompt_edit,
    size="1024x1536"
)

# Save the image to a file and resize/compress for smaller files
image_base64 = result_edit.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

image = Image.open(BytesIO(image_bytes))
image = image.resize((250, 375), Image.LANCZOS)
image.save(img_path_edit, format="JPEG", quality=80, optimize=True)

# Show the result
display(IPImage(img_path_edit))

```

### Edit an image with a mask

You can also provide a mask along with your input images (if there are several, the mask will be applied on the first one) to edit only the part of the input image that is not covered by the mask. Please note that the model might still edit some parts of the image inside the mask, but it will avoid it.

Important note: the mask should contain an alpha channel. If you're generating it manually, for example using an image editing software, make sure you include this alpha channel.

#### Generating a mask

For this example, we'll use our model to generate the mask automatically for us. The mask might not be exact, but it will be enough for our purposes. If you need to have an exact mask, feel free to use an image segmentation model.

```python

img_path_mask = "imgs/mask.png"
prompt_mask = "generate a mask delimiting the entire character in the picture, using white where the character is and black for the background. Return an image in the same size as the input image."

img_input = open(img_path1, "rb")

# Generate the mask
result_mask = client.images.edit(
    model="gpt-image-1",
    image=img_input,
    prompt=prompt_mask
)

# Save the image to a file and resize/compress for smaller files
image_base64 = result_mask.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

image = Image.open(BytesIO(image_bytes))
image = image.resize((300, 300), Image.LANCZOS)
image.save(img_path_mask, format="PNG")

# Show the mask
display(IPImage(img_path_mask))

```

#### Creating an alpha channel

This step is optional, if you want to turn a black & white image into a mask with an alpha channel that can be used in the Image Edit API.

```python

# 1. Load your black & white mask as a grayscale image
mask = Image.open(img_path_mask).convert("L")

# 2. Convert it to RGBA so it has space for an alpha channel
mask_rgba = mask.convert("RGBA")

# 3. Then use the mask itself to fill that alpha channel
mask_rgba.putalpha(mask)

# 4. Convert the mask into bytes
buf = BytesIO()
mask_rgba.save(buf, format="PNG")
mask_bytes = buf.getvalue()

# Save the resulting file
img_path_mask_alpha = "imgs/mask_alpha.png"
with open(img_path_mask_alpha, "wb") as f:
    f.write(mask_bytes)

```

#### Editing with the mask

When using a mask, we still need the prompt the model describing the entiring resulting image, not just the area that is masked.

```python

prompt_mask_edit = "A strange character on a colorful galaxy background, with lots of stars and planets."
mask = open(img_path_mask_alpha, "rb")

result_mask_edit = client.images.edit(
    model="gpt-image-1",
    prompt=prompt_mask_edit,
    image=img_input,
    mask=mask,
    size="1024x1024"
)

# Display result

img_path_mask_edit = "imgs/mask_edit.png"

image_base64 = result_mask_edit.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

image = Image.open(BytesIO(image_bytes))
image = image.resize((300, 300), Image.LANCZOS)
image.save(img_path_mask_edit, format="JPEG", quality=80, optimize=True)

display(IPImage(img_path_mask_edit))

```
