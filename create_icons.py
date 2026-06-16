from PIL import Image, ImageDraw

for size in [192, 512]:
    img = Image.new('RGB', (size, size), '#070b1a')
    draw = ImageDraw.Draw(img)
    margin = size // 8
    draw.ellipse([margin, margin, size-margin, size-margin], fill='#6366f1')
    img.save(f'tracker/static/icon-{size}.png')

print('Ikony utworzone!')