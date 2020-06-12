<template>

  <div id="wrapper">
    <v-container fluid>
      <v-row>
        <v-col
          v-for="photo in allPhotos"
          :key="photo.id"
          class="d-flex child-flex"
        >
          <h1>{{ photo.name }}</h1>
        </v-col>
      </v-row>
    </v-container>
  </div>

</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'Photos',
  computed: mapGetters(['allPhotos']),
};
</script>

<style scoped>
</style>
