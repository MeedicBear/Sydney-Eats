import re

with open('web/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace generateDateBtn logic
old_logic = re.search(r"generateDateBtn\.addEventListener\('click', \(\) => \{.*?(?=\n\}\);\n)", js, re.DOTALL).group(0) + '\n});\n'

new_logic = '''generateDateBtn.addEventListener('click', () => {
    dateResults.classList.add('hidden');
    dateError.classList.add('hidden');
    
    const maxDist = parseFloat(dateDistanceInput.value);
    const dateVibeSelect = document.getElementById('date-vibe-select');
    const selectedVibe = dateVibeSelect ? dateVibeSelect.value : 'Any';
    const dateStopsSelect = document.getElementById('date-stops-select');
    const numStops = dateStopsSelect ? parseInt(dateStopsSelect.value) : 2;
    
    // Separate pools
    const activities = places.filter(p => p.vibes.includes('🎡 Activity') || p.vibes.includes('🏖️ Beach'));
    const bars = places.filter(p => p.vibes.includes('🍸 Drinks & Bar'));
    let restaurants = places.filter(p => !p.vibes.includes('🎡 Activity') && !p.vibes.includes('🏖️ Beach'));
    
    if (selectedVibe !== 'Any') {
        restaurants = restaurants.filter(r => r.vibes.includes(selectedVibe));
    }
    
    // Shuffle activities to get random pairing
    const shuffledActivities = [...activities].sort(() => 0.5 - Math.random());
    
    let validPair = null;
    let validTrip = null;
    let totalDist = 0;
    
    for (const act of shuffledActivities) {
        if(!act.coordinates) continue;
        
        if (numStops === 2) {
            // Find all restaurants within maxDist
            const validRests = restaurants.filter(r => {
                if(!r.coordinates) return false;
                const dist = getDistanceFromLatLonInKm(act.coordinates.lat, act.coordinates.lng, r.coordinates.lat, r.coordinates.lng);
                return dist <= maxDist;
            });
            
            if (validRests.length > 0) {
                const chosenRest = validRests[Math.floor(Math.random() * validRests.length)];
                totalDist = getDistanceFromLatLonInKm(act.coordinates.lat, act.coordinates.lng, chosenRest.coordinates.lat, chosenRest.coordinates.lng);
                validTrip = [act, chosenRest];
                break;
            }
        } else if (numStops === 3) {
            // Find all bars within maxDist of act
            const validBars = bars.filter(b => {
                if(!b.coordinates || b.id === act.id) return false;
                const dist = getDistanceFromLatLonInKm(act.coordinates.lat, act.coordinates.lng, b.coordinates.lat, b.coordinates.lng);
                return dist <= maxDist;
            });
            
            let foundTrip = false;
            // Shuffle bars to randomize
            const shuffledBars = [...validBars].sort(() => 0.5 - Math.random());
            
            for (const bar of shuffledBars) {
                // Find restaurants within maxDist of bar
                const validRests = restaurants.filter(r => {
                    if(!r.coordinates || r.id === act.id || r.id === bar.id) return false;
                    const dist = getDistanceFromLatLonInKm(bar.coordinates.lat, bar.coordinates.lng, r.coordinates.lat, r.coordinates.lng);
                    return dist <= maxDist;
                });
                
                if (validRests.length > 0) {
                    const chosenRest = validRests[Math.floor(Math.random() * validRests.length)];
                    const d1 = getDistanceFromLatLonInKm(act.coordinates.lat, act.coordinates.lng, bar.coordinates.lat, bar.coordinates.lng);
                    const d2 = getDistanceFromLatLonInKm(bar.coordinates.lat, bar.coordinates.lng, chosenRest.coordinates.lat, chosenRest.coordinates.lng);
                    totalDist = d1 + d2;
                    validTrip = [act, bar, chosenRest];
                    foundTrip = true;
                    break;
                }
            }
            if (foundTrip) break;
        }
    }
    
    if (validTrip) {
        const container = document.getElementById('date-cards-container');
        container.className = `grid grid-cols-1 md:grid-cols-${validTrip.length} gap-6 relative`;
        
        container.innerHTML = validTrip.map((place, i) => {
            return `
                <div class="relative">
                    ${generateCardHTML(place)}
                    ${i < validTrip.length - 1 ? `
                        <div class="hidden md:flex absolute -right-6 top-1/2 transform -translate-y-1/2 items-center justify-center pointer-events-none z-10 w-8">
                            <div class="bg-white dark:bg-gray-800 rounded-full border-2 border-pink-200 dark:border-gray-600 shadow-sm text-lg">
                                ➡
                            </div>
                        </div>
                    ` : ''}
                </div>
            `;
        }).join('');
        
        document.getElementById('date-distance-calc').textContent = `Total travel distance: ${totalDist.toFixed(1)} km`;
        dateResults.classList.remove('hidden');
    } else {
        dateError.classList.remove('hidden');
    }
});
'''

js = js.replace(old_logic, new_logic)

with open('web/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
