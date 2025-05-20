<script lang="ts">
	import { onMount } from 'svelte';
	import Chart from 'chart.js/auto';
	import type { LegendItem } from 'chart.js';

	interface PredictionData {
		ds: string;
		yhat: number;
	}

	let canvas: HTMLCanvasElement;
	let chart: Chart;
	let labels: string[] = [];
	let fullscreen = false;

	export let city: string;

	let email = "mal.kdsov@gmail.com";

	function getAgeCategory(age: number): 'child' | 'adult' | 'senior' {
		if (age < 12) return 'child';
		if (age >= 65) return 'senior';
		return 'adult';
	}

	function getPollutantsByAge(age: number): string[] {
		const category = getAgeCategory(age);

		if (category === 'child') return ['PM25', 'NO2', 'O3', 'PM10'];
		if (category === 'senior') return ['PM25', 'PM10', 'O3', 'SO2'];

		return ['PM25'];
	}

	function getPollutantsForPathology(pathology: string): string[] {
		if (pathology === 'asthme') return ['PM25', 'NO2', 'O3'];
		if (pathology === 'bpco') return ['PM10', 'PM25'];
		if (pathology === 'bronchite chronique') return ['NO2'];
		if (pathology === 'enfant') return ['PM25', 'NO2', 'O3', 'PM10'];
		if (pathology === 'senior') return ['PM25', 'NO2', 'O3', 'PM10'];
		return ['PM25'];
	}

	function getCombinedPollutants(age: number, pathology?: string): string[] {
		const set = new Set(getPollutantsByAge(age));

		if (pathology) {
			getPollutantsForPathology(pathology).forEach(p => set.add(p));
		}

		return Array.from(set);
	}

	const dummyData = Array.from({ length: 24 }, (_, h) => ({
		ds: new Date(Date.now() + h * 3600000).toISOString(),
		yhat: Math.random() * 100
	}));

	function getColorForPollutant(pollutant: string): string {
		switch (pollutant) {
			case 'PM25': return 'blue';
			case 'NO2': return 'orange';
			case 'O3': return 'red';
			case 'PM10': return 'purple';
			case 'PollenLevel': return 'green';
			default: return 'gray';
		}
	}

	onMount(async () => {
		if (!city || city.trim().length === 0) {
		console.warn("City non définie au moment du montage du composant.");
		return;}

		try {
			const profileRes = await fetch(`http://localhost:5000/api/user/profile?email=${email}`);
			if (!profileRes.ok) throw new Error('Erreur chargement profil utilisateur');
			const { pathology } = await profileRes.json();

			const cityRes = await fetch(`http://localhost:5000/api/zones/by-city?city=${encodeURIComponent(city)}`);
			if (!cityRes.ok) throw new Error('Zone introuvable pour la ville : ' + city);
			const { zone_id } = await cityRes.json();

			const pollutants = getPollutantsForPathology(pathology);
			const datasets = [];
			let firstPollutantData: PredictionData[] = [];

			for (const [i, pollutant] of pollutants.entries()) {
				const res = await fetch(`http://localhost:5000/api/predict/zone?zone_id=${zone_id}&pollutant=${pollutant}`);
				if (!res.ok) throw new Error(`Erreur données pour ${pollutant}`);
				const data = await res.json();
				if (i === 0) {
					firstPollutantData = data;
				}

				datasets.push({
					label: pollutant,
					data: data.slice(0, 24).map((d: PredictionData) => d.yhat),
					borderColor: getColorForPollutant(pollutant),
					backgroundColor: `${getColorForPollutant(pollutant)}33`,
					tension: 0.4
				});
			}

			const labels = firstPollutantData.slice(0, 24).map(d => 
				new Date(d.ds).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
			);

			if (chart) chart.destroy();

			const data = dummyData.map(d => d.yhat);

			chart = new Chart(canvas, {
				type: 'line',
				data: { labels, datasets },
				options: {
					responsive: true,
					maintainAspectRatio: false,
					scales: {
						y: {
							beginAtZero: true,
							title: {
								display: true,
								text: 'Concentration (µg/m³ ou niveau)',
								font: { size: 14 }
							}
						},
						x: {
							title: {
								display: true,
								text: 'Heure de la journée',
								font: { size: 14 }
							},
							ticks: {
								autoSkip: true,
								maxTicksLimit: 12
							}
						}
					},
					plugins: {
						legend: {
							position: 'bottom',
							labels: {
								usePointStyle: true,
								padding: 14,
								generateLabels: function (chart) {
									const descriptions: Record<string, string> = {
										PM25: '→ PM2.5 : fines particules inhalables',
										PM10: '→ PM10 : particules plus grosses',
										NO2: '→ NO₂ : pollution liée au trafic',
										O3: '→ O₃ : formé par réaction au soleil',
										PollenLevel: '→ Pollen : allergènes végétaux',
										CO: '→ CO : monoxyde de carbone'
									};
									return chart.data.datasets.map((dataset, i) => {
										const key = dataset.label?.split(" ")[0] || 'Autre';
										return {
											text: descriptions[key] || dataset.label || 'Inconnu',
											fillStyle: dataset.borderColor as string,
											strokeStyle: dataset.borderColor as string,
											lineWidth: 2,
											hidden: !chart.isDatasetVisible(i),
											datasetIndex: i
										};
									});
								}
							}
						},
						title: {
							display: true,
							text: `Prévision à ${city} pour votre santé (${pathology.toUpperCase()})`,
							font: { size: 18 }
						},
						tooltip: {
							mode: 'index',
							intersect: false,
							callbacks: {
								label: function (ctx) {
									const label = ctx.dataset.label || '';
									return `${label} : ${ctx.formattedValue}`;
								}
							}
						}
					},
					interaction: {
						mode: 'nearest',
						axis: 'x',
						intersect: false
					}
				}
			});
		} catch (error) {
			console.error('Erreur chargement graphique :', error);
		}
	});
</script>

<div class={`relative ${fullscreen ? 'fixed inset-0 z-50 bg-white p-6' : 'rounded-lg shadow-md'} transition-all duration-300`}>

	<div class="w-full" style="height: 400px;">
		<canvas bind:this={canvas}></canvas>
	</div>
</div>

<style>
    .chart-container {
        position: relative;
        height: 400px; /* Augmentez cette valeur pour plus de hauteur */
        width: 100%;
        margin: 1rem 0;
    }
</style>