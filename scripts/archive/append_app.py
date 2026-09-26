append_text = """

// --- Date Creator Logic ---
const dateCreatorBtn = document.getElementById('date-creator-btn');
const dateModal = document.getElementById('date-modal');
const closeModalBtn = document.getElementById('close-modal-btn');
const dateDistanceInput = document.getElementById('date-distance');
const dateDistanceVal = document.getElementById('date-distance-val');
const generateDateBtn = document.getElementById('generate-date-btn');
const dateResults = document.getElementById('date-results');
const dateError = document.getElementById('date-error');

dateCreatorBtn.addEventListener('click', () => {
    dateModal.classList.remove('hidden');
});

closeModalBtn.addEventListener('click', () => {
    dateModal.classList.add('hidden');
});

dateDistanceInput.addEventListener('input', (e) => {
    dateDistanceVal.textContent = e.target.value + ' km';
});

function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
    const R = 6371; // Radius of the earth in km
    const dLat = deg2rad(lat2-lat1);
    const dLon = deg2rad(lon2-lon1); 
    const a = 
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * 
        Math.sin(dLon/2) * Math.sin(dLon/2); 
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
    return R * c; // Distance in km
}

function deg2rad(deg) {
    return deg * (Math.PI/180);
}

function generateCardHTML(place) {
    return `
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden h-full flex flex-col">
            ${place.imageUrl ? `<img src="${place.imageUrl}" alt="${place.name}" class="w-full h-40 object-cover">` : `<div class="w-full h-40 bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-gray-400">No Image</div>`}
            <div class="p-4 flex-1 flex flex-col">
                <h3 class="text-lg font-bold text-gray-900 dark:text-white leading-tight mb-1">${place.name}</h3>
                <p class="text-xs text-gray-500 dark:text-gray-400 mb-2">📍 ${place.location}</p>
                <div class="flex gap-1 mb-2 flex-wrap">
                    <span class="px-2 py-0.5 bg-green-100 text-green-800 text-[10px] font-semibold rounded">${place.price}</span>
                    ${place.vibes.slice(0,2).map(vibe => `<span class="px-2 py-0.5 bg-indigo-100 dark:bg-indigo-900 text-indigo-800 dark:text-indigo-200 text-[10px] rounded">${vibe}</span>`).join('')}
                </div>
                <p class="text-sm text-gray-700 dark:text-gray-300 mb-3 flex-1">${place.description || ''}</p>
                <div class="flex gap-3 mt-auto pt-2 border-t border-gray-100 dark:border-gray-700">
                    <a href="https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(place.name + ' ' + place.location)}" target="_blank" class="text-indigo-600 dark:text-indigo-400 hover:underline text-xs font-medium">📍 Maps</a>
                    ${place.url ? `<a href="${place.url}" target="_blank" class="text-pink-600 dark:text-pink-400 hover:underline text-xs font-medium">🎬 Watch Reel</a>` : (place.website ? `<a href="${place.website}" target="_blank" class="text-blue-600 dark:text-blue-400 hover:underline text-xs font-medium">🌐 Website</a>` : '')}
                </div>
            </div>
        </div>
    `;
}

generateDateBtn.addEventListener('click', () => {
    dateResults.classList.add('hidden');
    dateError.classList.add('hidden');
    
    const maxDist = parseFloat(dateDistanceInput.value);
    
    // Separate activities and restaurants
    const activities = places.filter(p => p.vibes.includes('🎡 Activity') || p.vibes.includes('🏖️ Beach'));
    const restaurants = places.filter(p => !p.vibes.includes('🎡 Activity') && !p.vibes.includes('🏖️ Beach'));
    
    // Shuffle activities to get random pairing
    const shuffledActivities = [...activities].sort(() => 0.5 - Math.random());
    
    let validPair = null;
    let calcDist = 0;
    
    for (const act of shuffledActivities) {
        if(!act.coordinates) continue;
        
        // Find all restaurants within maxDist
        const validRests = restaurants.filter(r => {
            if(!r.coordinates) return false;
            const dist = getDistanceFromLatLonInKm(act.coordinates.lat, act.coordinates.lng, r.coordinates.lat, r.coordinates.lng);
            return dist <= maxDist;
        });
        
        if (validRests.length > 0) {
            // Pick a random restaurant from the valid ones
            const chosenRest = validRests[Math.floor(Math.random() * validRests.length)];
            calcDist = getDistanceFromLatLonInKm(act.coordinates.lat, act.coordinates.lng, chosenRest.coordinates.lat, chosenRest.coordinates.lng);
            validPair = { act, rest: chosenRest };
            break;
        }
    }
    
    if (validPair) {
        document.getElementById('date-activity-card').innerHTML = generateCardHTML(validPair.act);
        document.getElementById('date-dinner-card').innerHTML = generateCardHTML(validPair.rest);
        document.getElementById('date-distance-calc').textContent = `These two spots are only ${calcDist.toFixed(1)} km apart!`;
        dateResults.classList.remove('hidden');
    } else {
        dateError.classList.remove('hidden');
    }
});
"""

with open('web/app.js', 'a', encoding='utf-8') as f:
    f.write(append_text)
