<script>
  import { onMount } from 'svelte';
  import L from 'leaflet';

  let map;

  // Données AQI simulées (tu pourras remplacer par une prop ou un fetch)
  let aqiData = [
    { city: "Mons, Belgium", aqi: 59, lat: 50.46519, lon: 3.93971 },
    { city: "Ukkel, Belgium", aqi: 53, lat: 50.79663, lon: 4.35853 },
    { city: "Gardanne, France", aqi: 27, lat: 43.45358, lon: 5.46667 },
    { city: "Fos Les Carabins, France", aqi: 5, lat: 43.45892, lon: 4.93457 },
    { city: "Besançon, France", aqi: 22, lat: 47.24762, lon: 6.01565 },
    { city: "Neuwied, Germany", aqi: 30, lat: 50.42869, lon: 7.46388 },
    { city: "Walshoutem, Belgium", aqi: 32, lat: 50.71170, lon: 5.10315 }
  ];

  const seuilUtilisateur = 50;

  function getColor(aqi) {
    if (aqi == null) return "#999";
    if (aqi <= 50) return "#00e400";
    if (aqi <= 100) return "#ffff00";
    if (aqi <= 150) return "#ff7e00";
    if (aqi <= 200) return "#ff0000";
    if (aqi <= 300) return "#8f3f97";
    return "#7e0023";
  }

  onMount(() => {
    map = L.map('map').setView([50.465, 3.94], 6);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    aqiData.forEach(loc => {
      const couleur = getColor(loc.aqi);
      const risque = loc.aqi >= seuilUtilisateur ? "⚠️ Risque élevé" : "🟢 Faible risque";

      const marker = L.circleMarker([loc.lat, loc.lon], {
        radius: 10,
        fillColor: couleur,
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
      }).addTo(map);

      marker.bindPopup(`
        <strong>${loc.city}</strong><br/>
        AQI : ${loc.aqi ?? "Indisponible"}<br/>
        ${risque}
      `);
    });
  });
</script>

<style>
  #map {
    height: 100vh;
    width: 100%;
  }
</style>

<div id="map"></div>
