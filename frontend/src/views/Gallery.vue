<template>
  <div class="wrapper">
    <v-container fluid>
      <v-row>
        <v-col
          v-for="photo in allPhotos"
          :key="photo.id"
          class="d-flex child-flex"
          :cols=3
        >
          <Photo :photo="photo" />
        </v-col>
      </v-row>
    </v-container>

  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import Photo from '../components/Photo.vue';

export default {
  name: 'Gallery',
  components: {
    Photo,
  },
  methods: {
    ...mapActions(['fetchPhotos']),
  },
  computed: mapGetters(['allPhotos']),
  created() {
    this.fetchPhotos();
  },
};
</script>
