<script lang="ts">
    import ChartComponent from '$lib/components/ChartComponent.svelte';
    import { page } from '$app/stores';

    let userCity: string | null = null;

    let city = '';
	$: city = $page.url.searchParams.get('city') ?? '';
</script>

<!-- <div class="chart-container">
    <ChartComponent city={userCity ?? ''} />
</div> -->

<div class="min-h-screen bg-white p-6">
	<a href="/" class="text-blue-600 underline mb-4 block">← Retour à la carte</a>
	<h1 class="text-2xl font-bold mb-4">Prévision pollution : {city}</h1>
	{#if city}
		<ChartComponent {city} />
	{:else}
		<p class="text-slate-600">Aucune ville sélectionnée</p>
	{/if}
</div>

<style>
    .chart-container {
        width: 800px;
        height: 400px;
        margin: 20px auto;
    }
</style>