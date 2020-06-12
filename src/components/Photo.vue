<template>

  <v-hover v-slot:default="{ hover }">
    <v-card
      :elevation="hover ? 12 : 2"
      :class="{ 'on-hover': hover }"
    >
      <v-img
        :src="photo.src"
        :lazy-src="photo.lazySrc"
        aspect-ratio="1"
        class="d-flex flex-row align-end"
      >
        <v-card-title class="title white--text pb-0">
          <v-row class="fill-height justify-end">
            <v-btn
              :class="{ 'show-btns': hover }"
              color="rgba(255, 255, 255, 0)"
              icon
            >
              <v-icon
                :class="{ 'show-btns': hover }"
                color="rgba(255, 255, 255, 0)"
              >
                {{photo.is_liked ? 'mdi-heart' : 'mdi-heart-outline'}}
              </v-icon>
            </v-btn>
          </v-row>
        </v-card-title>
        <template v-slot:placeholder>
          <v-row
            class="fill-height ma-0"
            align="center"
            justify="center"
          >
            <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
          </v-row>
        </template>
      </v-img>
    </v-card>
  </v-hover>

</template>

<script>
export default {
  name: 'Photos',
  props: ['photo'],
};
</script>

<style scoped>

.v-card {
  transition: .4s ease-in-out;
}

.v-card.on-hover {
  opacity: 0.8;
 }

.show-btns {
  color: rgba(255, 255, 255, 1) !important;
}

</style>
