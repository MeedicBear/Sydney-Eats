// App State
let places = [];
let savedSpots = JSON.parse(localStorage.getItem('savedSpots')) || [];
let map;
let markers = [];
let showMap = false;
let showingSavedOnly = false;

// DOM Elements
const placesGrid = document.getElementById('places-grid');
const searchInput = document.getElementById('search-input');
const priceFilters = document.querySelectorAll('.price-filter');
const vibeFiltersContainer = document.getElementById('vibe-filters');
const resultsCount = document.getElementById('results-count');
const toggleMapBtn = document.getElementById('toggle-map-btn');
const mapContainer = document.getElementById('map-container');

// Initialize Map
function initMap() {
    // Center roughly on Sydney
    map = L.map('map').setView([-33.8688, 151.2093], 12);
    
    L.tileLayer('https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}', {
        attribution: '&copy; <a href="https://www.google.com/intl/en_us/help/terms_maps.html">Google Maps</a>'
    }).addTo(map);
}

// Load Data
async function loadData() {
    try {
        // Initialize Shared List from URL
        const urlParams = new URLSearchParams(window.location.search);
        const sharedSaved = urlParams.get('saved');
        if (sharedSaved) {
            savedSpots = sharedSaved.split(',');
            localStorage.setItem('savedSpots', JSON.stringify(savedSpots));
            window.history.replaceState({}, document.title, window.location.pathname);
        }

        // Initialize Dark Mode
        if (localStorage.getItem('darkMode') === 'true') {
            document.documentElement.classList.add('dark');
            document.getElementById('dark-mode-btn').innerText = '☀️';
        }

        if (typeof processedPlacesData !== 'undefined' && processedPlacesData.length > 0) {
            places = processedPlacesData.sort(() => Math.random() - 0.5); // Randomize
        } else {
            places = getDummyData();
        }
        
        extractVibes();
        renderPlaces(places);
        updateMapMarkers(places);

    } catch (error) {
        alert("Data load error: " + error.stack);
        console.error("Failed to load data, loading dummy data instead", error);
        places = getDummyData();
        extractVibes();
        renderPlaces(places);
        updateMapMarkers(places);
    }
}

// Render Place Cards
function renderPlaces(data) {
    placesGrid.innerHTML = '';
    resultsCount.innerText = data.length;

    data.forEach(place => {
        const isSaved = savedSpots.includes(place.id);
        const card = document.createElement('div');
        card.className = 'bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow flex flex-col';
        
        card.innerHTML = `
            ${place.imageUrl ? `<img src="${place.imageUrl}" alt="${place.name}" class="w-full h-48 object-cover">` : `<div class="w-full h-48 bg-gray-200 flex items-center justify-center text-gray-400">No Image Available</div>`}
            <div class="p-5 flex-1 flex flex-col">
                <div class="flex justify-between items-start mb-2">
                    <h3 class="text-xl font-bold text-gray-900 leading-tight">${place.name}</h3>
                    <button class="save-btn text-2xl focus:outline-none" data-id="${place.id}">
                        ${isSaved ? '★' : '☆'}
                    </button>
                </div>
                <p class="text-sm text-gray-500 mb-3 flex items-center gap-1">
                    📍 ${place.location}
                </p>
                <div class="flex gap-2 mb-3 flex-wrap">
                    <span class="px-2 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded">${place.price}</span>
                    ${place.vibes.slice(0,3).map(vibe => `<span class="px-2 py-1 bg-indigo-100 text-indigo-800 text-xs rounded">${vibe}</span>`).join('')}
                </div>
                ${place.rating ? `<div class="text-sm font-bold text-yellow-500 mb-2 flex items-center gap-1">⭐ ${place.rating} <span class="text-xs text-gray-400 font-normal">(${place.reviewCount} reviews)</span></div>` : ''}
                <div class="flex gap-4 mt-auto pt-2 border-t border-gray-100">
                    <a href="https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(place.name + ' ' + place.location)}" target="_blank" class="text-indigo-600 hover:text-indigo-800 text-sm font-medium">📍 Maps</a>
                    ${place.url ? `<a href="${place.url}" target="_blank" class="text-pink-600 hover:text-pink-800 text-sm font-medium">🎬 Watch Reel</a>` : (place.website ? `<a href="${place.website}" target="_blank" class="text-blue-600 hover:text-blue-800 text-sm font-medium">🌐 Website</a>` : '')}
                </div>
            </div>
        `;
        placesGrid.appendChild(card);
    });

    // Attach event listeners for save buttons
    document.querySelectorAll('.save-btn').forEach(btn => {
        btn.addEventListener('click', (e) => toggleSave(e.target.dataset.id));
    });
}

// Map Markers
function updateMapMarkers(data) {
    if(!map) return;
    
    // Clear existing
    markers.forEach(m => map.removeLayer(m));
    markers = [];

    data.forEach(place => {
        if(place.coordinates && place.coordinates.lat && place.coordinates.lng) {
            let iconOptions = {};
            if (place.imageUrl) {
                const markerHtml = `<div style="background-image: url('${place.imageUrl}'); width: 40px; height: 40px; background-size: cover; background-position: center; border-radius: 50%; border: 3px solid #4f46e5; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3);"></div>`;
                iconOptions = { icon: L.divIcon({ html: markerHtml, className: 'custom-marker', iconSize: [40, 40], iconAnchor: [20, 20], popupAnchor: [0, -20] }) };
            }
            
            const mapLink = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(place.name + ' ' + place.location)}`;
            const popupContent = `
                <div class="text-center" style="width: 200px;">
                    ${place.imageUrl ? `<div style="background-image: url('${place.imageUrl}'); height: 120px; width: 100%; background-size: cover; background-position: center;" class="rounded mb-2"></div>` : ''}
                    <b class="text-base block mb-1 leading-tight">${place.name}</b>
                    <span class="text-gray-600 text-xs block mb-1">${place.location}</span>
                    <span class="text-green-600 font-bold text-sm block">${place.price}</span>
                    ${place.rating ? `<div class="text-xs font-bold text-yellow-600 dark:text-yellow-400 mt-1">⭐ ${place.rating} <span class="text-gray-400 font-normal">(${place.reviewCount})</span></div>` : ''}

                    <div class="flex justify-center gap-4 mt-2">
                        <a href="${mapLink}" target="_blank" class="text-indigo-600 dark:text-indigo-400 hover:underline text-xs">📍 Maps</a>
                        ${place.url ? `<a href="${place.url}" target="_blank" class="text-pink-600 dark:text-pink-400 hover:underline text-xs">🎬 Reel</a>` : (place.website ? `<a href="${place.website}" target="_blank" class="text-blue-600 dark:text-blue-400 hover:underline text-xs">🌐 Website</a>` : '')}
                    </div>
                </div>
            `;

            const marker = L.marker([place.coordinates.lat, place.coordinates.lng], iconOptions)
                .addTo(map)
                .bindPopup(popupContent, { maxWidth: 220, minWidth: 200 });
            markers.push(marker);
        }
    });
}

// Extract Vibes dynamically for filters
function extractVibes() {
    const allVibes = new Set();
    places.forEach(p => p.vibes.forEach(v => allVibes.add(v)));
    
    vibeFiltersContainer.innerHTML = Array.from(allVibes).map(vibe => `
        <label class="inline-flex items-center bg-gray-100 px-2 py-1 rounded cursor-pointer hover:bg-gray-200">
            <input type="checkbox" value="${vibe}" class="vibe-filter hidden">
            <span class="text-sm text-gray-700 select-none vibe-label">${vibe}</span>
        </label>
    `).join('');

    // Add listeners to new checkboxes
    document.querySelectorAll('.vibe-filter').forEach(cb => {
        cb.addEventListener('change', (e) => {
            const label = e.target.nextElementSibling;
            if(e.target.checked) {
                label.classList.add('bg-indigo-600', 'text-white');
                label.classList.remove('text-gray-700');
            } else {
                label.classList.remove('bg-indigo-600', 'text-white');
                label.classList.add('text-gray-700');
            }
            filterData();
        });
    });
}

// Filtering Logic
function filterData() {
    const query = searchInput.value.toLowerCase();
    
    const activePrices = Array.from(priceFilters)
        .filter(cb => cb.checked)
        .map(cb => cb.value);
        
    const activeVibes = Array.from(document.querySelectorAll('.vibe-filter'))
        .filter(cb => cb.checked)
        .map(cb => cb.value);

    const filtered = places.filter(place => {
        const matchQuery = place.name.toLowerCase().includes(query) || place.description.toLowerCase().includes(query) || place.location.toLowerCase().includes(query);
        const matchPrice = activePrices.length === 0 || activePrices.includes(place.price);
        const matchVibe = activeVibes.length === 0 || activeVibes.some(v => place.vibes.includes(v));
        const matchSaved = !showingSavedOnly || savedSpots.includes(place.id);
        
        return matchQuery && matchPrice && matchVibe && matchSaved;
    });

    renderPlaces(filtered);
    updateMapMarkers(filtered);
}

// Save functionality
function toggleSave(id) {
    const idx = savedSpots.indexOf(id);
    if(idx > -1) {
        savedSpots.splice(idx, 1);
    } else {
        savedSpots.push(id);
    }
    localStorage.setItem('savedSpots', JSON.stringify(savedSpots));
    
    // Re-render to update stars
    // In a real app we'd just update the specific DOM element for efficiency
    filterData(); 
}

// Event Listeners
searchInput.addEventListener('input', filterData);
priceFilters.forEach(cb => cb.addEventListener('change', filterData));

toggleMapBtn.addEventListener('click', () => {
    showMap = !showMap;
    if(showMap) {
        mapContainer.classList.remove('hidden');
        if(!map) initMap();
        setTimeout(() => map.invalidateSize(), 100); // Fix rendering issue
        updateMapMarkers(places);
    } else {
        mapContainer.classList.add('hidden');
    }
});

document.getElementById('view-saved-btn').addEventListener('click', (e) => {
    showingSavedOnly = !showingSavedOnly;
    if (showingSavedOnly) {
        e.target.classList.add('text-indigo-600', 'font-bold', 'dark:text-indigo-400');
        e.target.classList.remove('text-gray-600', 'font-medium', 'dark:text-gray-300');
        e.target.innerText = 'Show All Spots';
    } else {
        e.target.classList.remove('text-indigo-600', 'font-bold', 'dark:text-indigo-400');
        e.target.classList.add('text-gray-600', 'font-medium', 'dark:text-gray-300');
        e.target.innerText = 'Saved Spots';
    }
    filterData();
});

// Share List
document.getElementById('share-btn').addEventListener('click', () => {
    if(savedSpots.length === 0) {
        alert("You haven't saved any spots yet!");
        return;
    }
    const url = new URL(window.location.href);
    url.searchParams.set('saved', savedSpots.join(','));
    navigator.clipboard.writeText(url.href).then(() => {
        const btn = document.getElementById('share-btn');
        const oldText = btn.innerText;
        btn.innerText = "Copied! ✅";
        setTimeout(() => btn.innerText = oldText, 2000);
    });
});

// Dark Mode
document.getElementById('dark-mode-btn').addEventListener('click', () => {
    document.documentElement.classList.toggle('dark');
    const isDark = document.documentElement.classList.contains('dark');
    localStorage.setItem('darkMode', isDark);
    document.getElementById('dark-mode-btn').innerText = isDark ? '☀️' : '🌙';
});


// Dummy Data for testing before scraping
function getDummyData() {
    return [
        {
            id: "1",
            name: "Hubert",
            location: "CBD, Sydney",
            price: "$$$",
            vibes: ["Romantic", "French", "Jazz"],
            description: "A subterranean French restaurant featuring live jazz and an incredible wine list. Perfect for a special occasion.",
            url: "https://instagram.com/sydneyonourplate",
            coordinates: { lat: -33.8642, lng: 151.2107 }
        },
        {
            id: "2",
            name: "Frankie's Pizza",
            location: "Hunter St, CBD",
            price: "$",
            vibes: ["Dive Bar", "Pizza", "Rock"],
            description: "Iconic dive bar with pinball, great cheap pizza, and live rock music. Very loud, very fun.",
            url: "https://instagram.com/sydneyonourplate",
            coordinates: { lat: -33.8647, lng: 151.2091 }
        },
        {
            id: "3",
            name: "The Baxter Inn",
            location: "Clarence St, CBD",
            price: "$$",
            vibes: ["Cocktails", "Whisky", "Hidden"],
            description: "Hidden basement bar famous for its massive whisky collection and classic cocktails. Pretzels on arrival.",
            url: "https://instagram.com/sydneyonourplate",
            coordinates: { lat: -33.8681, lng: 151.2053 }
        }
    ];
}

// Init
document.addEventListener('DOMContentLoaded', loadData);


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
                <div class="relative h-full">
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
