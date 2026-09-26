import re

with open('web/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_modal = re.search(r'<!-- Date Creator Modal -->.*?(?=<!-- Leaflet JS -->)', html, re.DOTALL).group(0)

new_modal = '''<!-- Date Creator Modal -->
    <div id="date-modal" class="fixed inset-0 bg-black bg-opacity-50 z-[100] hidden flex items-center justify-center p-4">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-2xl max-w-5xl w-full max-h-[90vh] overflow-y-auto p-6 relative transition-colors duration-200">
            <button id="close-modal-btn" class="absolute top-4 right-4 text-gray-500 hover:text-gray-800 dark:hover:text-white text-2xl font-bold">&times;</button>
            
            <h2 class="text-3xl font-bold text-center text-pink-600 dark:text-pink-400 mb-2">💘 Perfect Date Creator</h2>
            <p class="text-center text-gray-600 dark:text-gray-300 mb-6">Let us randomly generate the perfect pairing for your next outing.</p>
            
            <div class="flex flex-wrap gap-4 mb-8 items-end justify-center bg-pink-50 dark:bg-gray-700 p-4 rounded-lg">
                <div class="flex flex-col">
                    <label class="font-semibold text-sm mb-1 text-gray-700 dark:text-gray-200">Stops:</label>
                    <select id="date-stops-select" class="w-40 p-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 text-sm">
                        <option value="2">2 Stops (Act + Food)</option>
                        <option value="3">3 Stops (+ Bar)</option>
                    </select>
                </div>
                <div class="flex flex-col">
                    <label class="font-semibold text-sm mb-1 text-gray-700 dark:text-gray-200">Max Distance (km):</label>
                    <input type="range" id="date-distance" min="1" max="20" value="5" class="w-32 mb-1">
                    <span id="date-distance-val" class="text-center text-xs text-gray-600 dark:text-gray-300">5 km</span>
                </div>
                <div class="flex flex-col">
                    <label class="font-semibold text-sm mb-1 text-gray-700 dark:text-gray-200">Dinner Vibe:</label>
                    <select id="date-vibe-select" class="w-40 p-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 text-sm">
                        <option value="Any">Any Vibe</option>
                        <option value="🍷 Date Night">🍷 Date Night</option>
                        <option value="🤫 Hidden Gem">🤫 Hidden Gem</option>
                        <option value="🌅 Great Views">🌅 Great Views</option>
                        <option value="🍝 Good Food">🍝 Good Food</option>
                        <option value="🍸 Drinks & Bar">🍸 Drinks & Bar</option>
                        <option value="💸 Cheap Eats">💸 Cheap Eats</option>
                    </select>
                </div>
                <button id="generate-date-btn" class="bg-pink-600 hover:bg-pink-700 text-white font-bold py-2 px-6 rounded-lg shadow-lg transform transition hover:scale-105">
                    Generate!
                </button>
            </div>
            
            <div id="date-results" class="hidden">
                <h3 class="text-xl font-bold text-center mb-6 text-gray-800 dark:text-white" id="date-title">Your Custom Itinerary</h3>
                <div id="date-cards-container" class="grid grid-cols-1 md:grid-cols-2 gap-6 relative">
                    <!-- Cards injected here -->
                </div>
                <p id="date-distance-calc" class="text-center mt-6 font-semibold text-indigo-600 dark:text-indigo-400"></p>
            </div>
            
            <div id="date-error" class="hidden text-center text-red-500 font-bold p-6">
                Couldn't find a matching itinerary within that distance! Try increasing the radius or changing the vibe.
            </div>
        </div>
    </div>
    
    '''

html = html.replace(old_modal, new_modal)

with open('web/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
