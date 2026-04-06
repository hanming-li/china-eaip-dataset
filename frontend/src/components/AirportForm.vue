<template>
  <select class="form-select" multiple v-model="store.selectedAirportsHeliports">
    <option
      :key="id"
      :value="airport"
      class="monospace"
      v-for="[id, airport] of store.allAirportsHeliports"
    >
      {{ airport.properties.icao }} {{ airport.properties.iata }} {{ airport.properties.city }} /
      {{ airport.properties.name }}
    </option>
  </select>

  <AirportHint
    :airport="airport"
    :key="idx"
    class="my-1"
    v-for="(airport, idx) in store.selectedAirportsHeliports"
  />
</template>

<script setup lang="ts">
import { useGreatCircleMapStore } from '@/stores/GreatCircleMap'
import { onMounted } from 'vue'
import AirportHint from './AirportHint.vue'

const store = useGreatCircleMapStore()

onMounted(async function () {
  const response = await fetch(`/api/airports-heliports`)
  for (const airport of await response.json()) store.allAirportsHeliports.set(airport.id, airport)
})
</script>
