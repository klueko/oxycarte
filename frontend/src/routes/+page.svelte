<script lang="ts">
	import { onMount, tick } from 'svelte';
	import { page } from '$app/stores';
	import 'leaflet/dist/leaflet.css';
    import 'leaflet-fullscreen/dist/leaflet.fullscreen.css';
	import type * as LType from 'leaflet';
	import ChartComponent from '$lib/components/ChartComponent.svelte';

	let map: LType.Map;
	let L: typeof LType;
	let selectedCity: string | null = null;
	let isLoading = true;
	let cityData: CityData[] = [];
	let mapContainer: HTMLDivElement | null = null;
	let userCity: string | null = null;

	$: city = $page.url.searchParams.get('city') ?? '';
	
	const aqiCategories = [
		{ min: 0, max: 50, color: '#10b981', label: 'Bon', textColor: 'text-emerald-500' },
		{ min: 51, max: 100, color: '#f59e0b', label: 'Modéré', textColor: 'text-amber-500' },
		{ min: 101, max: 500, color: '#ef4444', label: 'Mauvais', textColor: 'text-red-500' }
	];

	const getAqiInfo = (aqi: number) => {
		return aqiCategories.find(cat => aqi >= cat.min && aqi <= cat.max) || aqiCategories[0];
	};

	const getColor = (aqi: number): string => {
		return getAqiInfo(aqi).color;
	};

	type CityData = {
		City: string;
		Avg_AQI: number;
		Avg_PM25: number;
		Avg_NO2: number;
		Latitude: number;
		Longitude: number;
	};

	const loadMap = async () => {
		try {
			const response = await fetch('http://localhost:5000/api/pollution/avg-by-city');
			cityData = await response.json();

			if (!mapContainer) return;
			map = L.map(mapContainer, {
				zoomControl: true,
				scrollWheelZoom: true,
				doubleClickZoom: true,
				dragging: true,
			}).setView([46.8, 2.2], 6);

			// @ts-ignore
			L.control.fullscreen({ position: 'topleft' }).addTo(map);


			L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
				attribution: '© OpenStreetMap contributors'
			}).addTo(map);

			cityData.forEach((city: CityData) => {
				const aqi = city.Avg_AQI;
				const aqiInfo = getAqiInfo(aqi);
				const color = aqiInfo.color;

				const marker = L.circleMarker([city.Latitude, city.Longitude], {
					color,
					fillColor: color,
					fillOpacity: 0.7,
					radius: 12,
					weight: 2
				}).addTo(map);

				marker.bindPopup(`
					<div class="font-sans p-1">
						<div class="font-bold text-lg mb-1">${city.City}</div>
						<div class="flex items-center gap-1 mb-1">
							<span class="inline-block w-3 h-3 rounded-full" style="background-color: ${color}"></span>
							<span class="font-medium">IQA: ${Math.round(aqi)} (${aqiInfo.label})</span>
						</div>
						<div class="text-sm">
							<div>PM<sub>2.5</sub>: ${city.Avg_PM25.toFixed(1)} µg/m³</div>
							<div>NO<sub>2</sub>: ${city.Avg_NO2.toFixed(1)} µg/m³</div>
						</div>
					</div>
				`);

				marker.on('click', () => {
					selectedCity = city.City;
				});
			});
		} catch (error) {
			console.error('Erreur lors du chargement des données:', error);
		} finally {
			isLoading = false;
		}
	};

	onMount(async () => {
		L = (await import('leaflet')).default;
		await import('leaflet-fullscreen');
		const res = await fetch('http://localhost:5000/api/user/profile?email=mal.kdsov@gmail.com');
		if (res.ok) {
			const { city } = await res.json();
			userCity = city;
		}
		await tick();
		await loadMap();
	});
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
	<div class="max-w-[110rem] mx-auto px-4 sm:px-6 lg:px-12 py-8">
		<header class="mb-10 text-center">
			<h1 class="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
				Oxycarte
			</h1>
			<h3 class="mt-3 text-lg text-slate-600 max-w-2xl mx-auto">Qualité de l'air en France</h3>
			<p class="mt-3 text-lg text-slate-600 max-w-2xl mx-auto">
				Visualisez la pollution atmosphérique actuelle et accédez aux prévisions pour les principales villes françaises.
			</p>
		</header>

		<div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
			<!-- Carte principale -->
			<div class="md:col-span-7 lg:col-span-8 bg-white rounded-xl shadow-lg overflow-hidden">
				<div class="p-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white flex justify-between items-center">
					<h2 class="text-xl font-semibold">Carte interactive</h2>
					<div class="flex items-center space-x-2 text-sm">
						{#each aqiCategories as category}
							<div class="flex items-center">
								<span class="inline-block w-3 h-3 rounded-full mr-1" style="background-color: {category.color}"></span>
								<span class="hidden sm:inline">{category.label}</span>
							</div>
						{/each}
					</div>
				</div>
					<div id="map" class="z-0" bind:this={mapContainer}></div>
				<div class="p-4 text-sm text-slate-500 border-t border-slate-100">
					Cliquez sur un marqueur pour voir les détails et prévisions pour la ville sélectionnée
				</div>
			</div>

			<!-- Panneau latéral d'informations -->
			<div class="md:col-span-7 lg:col-span-4 space-y-6 overflow-y-auto max-h-[calc(100vh-10rem)] px-2">
				<!-- Résumé de qualité de l'air -->
				<div class="bg-white rounded-xl shadow-lg overflow-hidden">
					<div class="p-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
						<h2 class="text-xl font-semibold">Information détaillée</h2>
					</div>
					
					{#if selectedCity}
						{#each cityData.filter(city => city.City === selectedCity) as city}
							{@const aqiInfo = getAqiInfo(city.Avg_AQI)}
							<div class="p-5">
								<div class="flex items-center justify-between mb-4">
									<h3 class="text-xl font-bold text-slate-800">{city.City}</h3>
									<span class={`px-3 py-1 rounded-full text-sm font-medium ${aqiInfo.textColor}`}>
										{aqiInfo.label}
									</span>
								</div>
								
								<div class="space-y-4">
									<div>
										<div class="flex justify-between mb-1">
											<span class="text-slate-600">Indice de qualité de l'air</span>
											<span class="font-medium">{Math.round(city.Avg_AQI)}</span>
										</div>
										<div class="w-full bg-slate-200 rounded-full h-2.5">
											<div class="h-2.5 rounded-full" style="width: {Math.min(100, city.Avg_AQI/5)}%; background-color: {aqiInfo.color}"></div>
										</div>
									</div>
									
									<div class="grid grid-cols-2 gap-4">
										<div class="bg-slate-50 p-3 rounded-lg">
											<div class="text-slate-500 text-sm">PM<sub>2.5</sub></div>
											<div class="text-slate-800 font-bold text-lg">{city.Avg_PM25.toFixed(1)}</div>
											<div class="text-xs text-slate-500">µg/m³</div>
										</div>
										<div class="bg-slate-50 p-3 rounded-lg">
											<div class="text-slate-500 text-sm">NO<sub>2</sub></div>
											<div class="text-slate-800 font-bold text-lg">{city.Avg_NO2.toFixed(1)}</div>
											<div class="text-xs text-slate-500">µg/m³</div>
										</div>
									</div>
									
									<div class="pt-4">
										<h4 class="font-medium text-slate-700 mb-2">Recommandations</h4>
										{#if city.Avg_AQI < 50}
											<p class="text-sm text-slate-600">La qualité de l'air est bonne. Idéal pour les activités en plein air.</p>
										{:else if city.Avg_AQI < 100}
											<p class="text-sm text-slate-600">Qualité acceptable. Les personnes sensibles devraient limiter l'effort prolongé en extérieur.</p>
										{:else}
											<p class="text-sm text-slate-600">Qualité d'air dégradée. Évitez les activités intenses en extérieur et gardez les fenêtres fermées.</p>
										{/if}
									</div>
								</div>
							</div>
						{/each}
					{:else}
						<div class="p-5 text-center">
							<svg class="w-12 h-12 mx-auto text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"></path>
							</svg>
							<p class="mt-2 text-slate-600">Sélectionnez une ville sur la carte pour voir les données détaillées</p>
						</div>
					{/if}
				</div>
				
				<!-- Widget de prévision -->
				<div class="bg-white rounded-xl shadow-lg overflow-hidden">
					<a
						href={`/graph?city=${encodeURIComponent(selectedCity ?? '')}`}
						class="block p-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:underline hover:opacity-90"
					>
						<h2 class="text-xl font-semibold">
							Prévisions – {selectedCity}
							<span class="ml-2 text-sm font-light">(Agrandir)</span>
						</h2>
					</a>

					{#if selectedCity}
						<div class="w-full" style="height: 400px;" >
							{#key selectedCity}
								<ChartComponent city={selectedCity} />
							{/key}
						</div>
					{:else}
						<div class="p-5 text-center text-slate-500">
							<p>Sélectionnez une ville pour voir les prévisions</p>
						</div>
					{/if}
				</div>
			</div>
		</div>

		<!-- Section d'information -->
		<div class="mt-12 bg-white rounded-xl shadow-lg overflow-hidden">
			<div class="p-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
				<h2 class="text-xl font-semibold">Comprendre l'indice de qualité de l'air</h2>
			</div>
			
			<div class="p-6">
				<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
					{#each aqiCategories as category}
						<div class="border rounded-lg p-4 flex items-center space-x-3">
							<div class="w-6 h-6 rounded-full" style="background-color: {category.color}"></div>
							<div>
								<div class="font-medium">{category.label}</div>
								<div class="text-sm text-slate-500">{category.min} - {category.max}</div>
							</div>
						</div>
					{/each}
				</div>
				
				<div class="mt-6 text-slate-600">
					<p>L'indice de qualité de l'air (IQA) est calculé à partir des concentrations de plusieurs polluants, dont les particules fines (PM2.5), le dioxyde d'azote (NO₂), l'ozone (O₃) et d'autres. Plus l'indice est élevé, plus la pollution atmosphérique est importante et plus elle présente un risque pour la santé.</p>
				</div>
			</div>
		</div>
		
		<footer class="mt-12 text-center text-slate-500 text-sm">
			<p>© {new Date().getFullYear()} Oxycarte • Données actualisées toutes les heures</p>
		</footer>
	</div>
</div>

<style>
	#map {
		height: 75vh;
		width: 100%;
	}
	
	:global(.leaflet-popup-content-wrapper) {
		border-radius: 0.5rem;
		box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
	}
	
	:global(.leaflet-popup-content) {
		margin: 0.75rem;
	}
</style>
