import re

with open('web/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# I need to completely replace generateDateBtn listener again
old_logic_pattern = r"generateDateBtn\.addEventListener\('click', \(\) => \{.*?\}\);\n"
old_logic_match = re.search(old_logic_pattern, js, re.DOTALL)
if old_logic_match:
    old_logic = old_logic_match.group(0)
else:
    print("Could not find old logic")

new_logic = '''generateDateBtn.addEventListener('click', () => {
    dateResults.classList.add('hidden');
    dateError.classList.add('hidden');
    
    const maxDist = parseFloat(dateDistanceInput.value);
    const dateVibeSelect = document.getElementById('date-vibe-select');
    const selectedVibe = dateVibeSelect ? dateVibeSelect.value : 'Any';
    const dateStopsSelect = document.getElementById('date-stops-select');
    const tripType = dateStopsSelect ? dateStopsSelect.value : '2';
    
    // Separate pools
    const activities = places.filter(p => p.vibes.includes('🎡 Activity') || p.vibes.includes('🏖️ Beach'));
    const bars = places.filter(p => p.vibes.includes('🍸 Drinks & Bar'));
    let restaurants = places.filter(p => !p.vibes.includes('🎡 Activity') && !p.vibes.includes('🏖️ Beach'));
    
    if (selectedVibe !== 'Any') {
        restaurants = restaurants.filter(r => r.vibes.includes(selectedVibe));
    }
    
    // Shuffle activities to get random pairing
    const shuffledActivities = [...activities].sort(() => 0.5 - Math.random());
    const shuffledBars = [...bars].sort(() => 0.5 - Math.random());
    
    let validTrip = null;
    let totalDist = 0;
    
    if (tripType === '2' || tripType === '3') {
        for (const act of shuffledActivities) {
            if(!act.coordinates) continue;
            
            if (tripType === '2') {
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
            } else if (tripType === '3') {
                // Find all bars within maxDist of act
                const validBarsAct = bars.filter(b => {
                    if(!b.coordinates || b.id === act.id) return false;
                    const dist = getDistanceFromLatLonInKm(act.coordinates.lat, act.coordinates.lng, b.coordinates.lat, b.coordinates.lng);
                    return dist <= maxDist;
                });
                
                let foundTrip = false;
                const shuffledBarsAct = [...validBarsAct].sort(() => 0.5 - Math.random());
                
                for (const bar of shuffledBarsAct) {
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
    } else if (tripType.startsWith('bar')) {
        const crawlLength = parseInt(tripType.replace('bar', ''));
        
        for (const startBar of shuffledBars) {
            if(!startBar.coordinates) continue;
            
            let currentCrawl = [startBar];
            let currentDist = 0;
            
            for(let step=1; step<crawlLength; step++) {
                const prevBar = currentCrawl[currentCrawl.length-1];
                const validNext = bars.filter(b => {
                    if(!b.coordinates || currentCrawl.find(c => c.id === b.id)) return false;
                    const dist = getDistanceFromLatLonInKm(prevBar.coordinates.lat, prevBar.coordinates.lng, b.coordinates.lat, b.coordinates.lng);
                    return dist <= maxDist;
                });
                
                if (validNext.length > 0) {
                    const nextBar = validNext[Math.floor(Math.random() * validNext.length)];
                    currentDist += getDistanceFromLatLonInKm(prevBar.coordinates.lat, prevBar.coordinates.lng, nextBar.coordinates.lat, nextBar.coordinates.lng);
                    currentCrawl.push(nextBar);
                } else {
                    break;
                }
            }
            
            if (currentCrawl.length === crawlLength) {
                validTrip = currentCrawl;
                totalDist = currentDist;
                break;
            }
        }
    }
    
    if (validTrip) {
        const container = document.getElementById('date-cards-container');
        // If 4 cards, use grid-cols-4 or grid-cols-2 depending on screen
        const cols = validTrip.length === 4 ? '4' : validTrip.length;
        container.className = `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-${cols} gap-6 relative`;
        
        container.innerHTML = validTrip.map((place, i) => {
            return `
                <div class="relative">
                    ${generateCardHTML(place)}
                    ${i < validTrip.length - 1 ? `
                        <div class="hidden lg:flex absolute -right-6 top-1/2 transform -translate-y-1/2 items-center justify-center pointer-events-none z-10 w-8">
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

if old_logic_match:
    js = js.replace(old_logic, new_logic)

with open('web/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
