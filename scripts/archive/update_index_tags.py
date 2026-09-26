import re

with open('web/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace checkboxes in the sidebar
mappings = {
    "🍝 Good Food": "🍽️ Great Dining",
    "🍔 Comfort & Quick": "🍔 Burgers & Fast Food",
}

for old, new in mappings.items():
    html = html.replace(f'value="{old}"', f'value="{new}"')
    html = html.replace(f'<span>{old}</span>', f'<span>{new}</span>')
    html = html.replace(f'>{old}<', f'>{new}<')

with open('web/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html tags")
