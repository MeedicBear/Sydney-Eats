import re

with open('web/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_stops = """<select id="date-stops-select" class="w-40 p-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 text-sm">
                        <option value="2">2 Stops (Act + Food)</option>
                        <option value="3">3 Stops (+ Bar)</option>
                    </select>"""

new_stops = """<select id="date-stops-select" class="w-48 p-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 text-sm">
                        <option value="2">2 Stops (Act + Food)</option>
                        <option value="3">3 Stops (Act + Bar + Food)</option>
                        <option value="bar3">3 Bars (Bar Crawl)</option>
                        <option value="bar4">4 Bars (Epic Crawl)</option>
                    </select>"""

if old_stops in html:
    html = html.replace(old_stops, new_stops)
else:
    print("Could not find old stops")

html = html.replace('💘 Perfect Date Creator', '💘 Itinerary & Crawl Creator')
html = html.replace('Date Creator 💘', 'Itineraries & Crawls 🍻')

with open('web/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
