path = r'c:\Users\phanm\Downloads\220334_TIEN_PHONG_TT_VL_2026\frontend\components\History.tsx'
with open(path, encoding='utf-8') as f:
    content = f.read()

content_normalized = content.replace('\r\n', '\n')
lines = content_normalized.split('\n')

# Print lines around 456-462 to confirm
for i in range(454, 463):
    print(f"Line {i+1}: {repr(lines[i])}")
