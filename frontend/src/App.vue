<template>
  <!-- header -->
  <maker-header class="mb-4" />

  <!-- app -->
  <div class="container">
    <csv-maker />
  </div>
</template>

<script>
import MakerHeader from '@/components/MakerHeader.vue'
import CsvMaker from '@/components/CsvMaker.vue'

export default {
  components: {
    MakerHeader,
    CsvMaker
  },
  name: 'App',
}
</script>

<style>
#app {
  text-align: center;
}
</style>
