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
import Photo from '@/components/Photo.vue'; // @ is an alias to /src
import { mapGetters, mapActions } from 'vuex';

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
