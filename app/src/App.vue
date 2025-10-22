<template>
  <Suspense>
    <template #default>
      <PredictionMarkets />
    </template>
    <template #fallback>
      <div class="flex items-center justify-center h-screen">
        <div class="spinner">Loading...</div>
      </div>
    </template>
  </Suspense>
</template>

<script setup>
import PredictionMarkets from "./components/PredictionMarkets.vue";
</script>
