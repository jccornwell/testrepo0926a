from PIL import Image

# Load image
img = Image.open('assets/bulldog_photo.jpg').convert('RGBA')
width, height = img.size
pixels = img.load()

# Parameters
# We'll detect green-ish pixels by checking hue or by comparing channels.
# Simple approach: if G is significantly larger than R and B, shift hue toward blue by swapping/mixing.

for y in range(height):
    for x in range(width):
        r, g, b, a = pixels[x, y]
        # skip transparent
        if a == 0:
            continue
        # detect green dominance
        if g > 1.15 * r and g > 1.15 * b and g > 40:
            # compute how 'green' it is (0..1)
            strength = min(1.0, (g - max(r, b)) / 120.0)
            # target blue color (keeping luminosity)
            # reduce green, increase blue
            new_r = int(r * (1 - 0.2 * strength))
            new_g = int(g * (1 - 0.9 * strength))
            new_b = int(min(255, b + 120 * strength))
            pixels[x, y] = (new_r, new_g, new_b, a)

# JPEG does not support alpha; convert to RGB (composite over white) before saving
try:
    rgb = Image.new('RGB', img.size, (255, 255, 255))
    rgb.paste(img, mask=img.split()[3])  # paste using alpha channel as mask
    rgb.save('assets/bulldog_bluegrass.jpg', quality=95)
    print('Saved assets/bulldog_bluegrass.jpg')
except Exception as e:
    print('Failed to save assets/bulldog_bluegrass.jpg:', e)
