<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title" v-if="airport.properties.city === airport.properties.name">
        {{ airport.properties.city }}
      </h5>
      <h5 class="card-title" v-else>
        {{ airport.properties.city }} / {{ airport.properties.name }}
      </h5>
      <h6 class="card-subtitle mb-2 text-body-secondary">
        {{ airport.properties.iata }} / {{ airport.properties.icao }}
      </h6>
      <h6 class="card-subtitle mb-2 text-body-secondary">
        {{ airport.geometry.coordinates[1] }}°N, {{ airport.geometry.coordinates[0] }}°E
      </h6>
      <p class="card-text"></p>
      <table class="table spread">
        <tbody>
          <tr>
            <th>Field Elevation</th>
            <td>{{ airport.geometry.coordinates[2] }} m</td>
          </tr>
          <tr>
            <th>Reference Temperature</th>
            <td>{{ airport.properties.reference_temperature_in_celcius }}℃</td>
          </tr>
          <tr>
            <th>Magnetic Variation</th>
            <td>{{ airport.properties.magnetic_variation }}°</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
<script setup lang="ts">
import type { 机场 } from '@/stores/types'
defineProps<{ airport: 机场 }>()
</script>
<style scoped>
.spread td {
  text-align: end;
}
</style>
