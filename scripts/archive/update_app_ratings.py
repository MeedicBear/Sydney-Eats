import re

with open('web/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update main card html
card_find = '''<div class="flex gap-2 mb-3 flex-wrap">
                    <span class="px-2 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded">${place.price}</span>
                    ${place.vibes.slice(0,3).map(vibe => \`<span class="px-2 py-1 bg-indigo-100 text-indigo-800 text-xs rounded">${vibe}</span>\`).join('')}
                </div>'''

card_replace = card_find + '''
                ${place.rating ? `<div class="text-sm font-bold text-yellow-600 dark:text-yellow-400 mb-2 flex items-center gap-1">⭐ ${place.rating} <span class="text-xs text-gray-400 font-normal">(${place.reviewCount} reviews)</span></div>` : ''}
'''

js = js.replace(card_find, card_replace)

# Update map popup html
popup_find = '''<span class="text-green-600 font-bold text-sm block">${place.price}</span>'''
popup_replace = popup_find + '''
                    ${place.rating ? `<div class="text-xs font-bold text-yellow-600 dark:text-yellow-400 mt-1">⭐ ${place.rating} <span class="text-gray-400 font-normal">(${place.reviewCount})</span></div>` : ''}
'''
js = js.replace(popup_find, popup_replace)

# Update date creator card html
date_card_find = '''<div class="flex gap-1 mb-2 flex-wrap">
                    <span class="px-2 py-0.5 bg-green-100 text-green-800 text-[10px] font-semibold rounded">${place.price}</span>
                    ${place.vibes.slice(0,2).map(vibe => \`<span class="px-2 py-0.5 bg-indigo-100 dark:bg-indigo-900 text-indigo-800 dark:text-indigo-200 text-[10px] rounded">${vibe}</span>\`).join('')}
                </div>'''
date_card_replace = date_card_find + '''
                ${place.rating ? `<div class="text-xs font-bold text-yellow-600 dark:text-yellow-400 mb-2">⭐ ${place.rating}</div>` : ''}
'''
js = js.replace(date_card_find, date_card_replace)

with open('web/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated app.js with ratings")
