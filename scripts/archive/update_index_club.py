import re

with open('web/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_checkbox = '''<label class="flex items-center space-x-2 text-sm text-gray-700 dark:text-gray-300">
                        <input type="checkbox" value="🪩 Nightclub" class="vibe-checkbox rounded border-gray-300">
                        <span>🪩 Nightclub</span>
                    </label>
                    <label class="flex items-center space-x-2 text-sm text-gray-700 dark:text-gray-300">'''

html = html.replace('<label class="flex items-center space-x-2 text-sm text-gray-700 dark:text-gray-300">', new_checkbox, 1)

with open('web/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
