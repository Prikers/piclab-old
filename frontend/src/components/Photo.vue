<template>
  <div v-bind:class="flipped ? 'flip-container flipped': 'flip-container'">
    <div class="flipper">
      <div class="front">
        <!-- Front Face of the Photo Card -->
        <v-hover v-slot:default="{ hover }">
          <v-card
            :elevation="hover ? 12 : 2"
            :class="{ 'on-hover': hover }"
          >
            <v-img
              :src="photo.thumbnail"
              aspect-ratio="1"
              class="d-flex flex-row align-end"
            >
                <div class="d-flex flow-column">
                  <v-btn
                    @click="flipped=true"
                    :class="{ 'show-btns': hover }"
                    color="rgba(255, 255, 255, 0)"
                    icon
                  >
                    <v-icon
                      :class="{ 'show-btns': hover }"
                      color="rgba(255, 255, 255, 0)"
                    >
                      mdi-dots-vertical
                    </v-icon>
                  </v-btn>
                  <v-spacer></v-spacer>
                  <v-btn
                    @click="toggleLikePhoto(photo)"
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
                </div>
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
      </div>
      <div class="back" style="height:100%">
        <!-- Back Face of the Photo Card -->
        <v-card
          elevation="12"
          height="100%"
          class="d-flex flex-column"
        >
          <!-- Modal for delete button -->
          <v-dialog v-model="dialogDeletePhoto" max-width="500">
            <template v-slot:activator="{ on, attrs }">
              <v-btn small absolute fab top right style="top: 10px;"
                @click="dialogDeletePhoto=true"
                v-bind="attrs"
                v-on="on"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
            <v-card>
              <v-card-title class="headline">
                Are you sure you want to delete?
              </v-card-title>
              <v-card-text>
                It will delete {{ photo.name }}. This action cannot be undone.
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn @click="dialogDeletePhoto = false">
                  Cancel
                </v-btn>
                <v-btn color="error" @click="handleDeletePhoto(photo)">
                  Yes, delete!
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <!-- List of main exif information -->
          <v-list dense class="ml-4">
            <v-subheader>{{ photo.name }}</v-subheader>
            <v-list-item dense>
              <v-list-item-icon>
                <v-icon>mdi-calendar-blank</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>
                  {{ photo.datetime_photo.date }}
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-clock</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>
                  {{ photo.datetime_photo.time }}
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-map-marker</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>Paris, France</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-camera</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>
                  {{ photo.camera }}
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-image-size-select-actual</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>
                  {{ `${photo.width} x ${photo.height} px (${photo.file_size_hr})`}}
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
          <v-spacer></v-spacer>
          <div class="d-flex flow-column">
            <v-btn icon @click="flipped=false">
              <v-icon>
                mdi-arrow-left
              </v-icon>
            </v-btn>
            <v-spacer></v-spacer>
            <!-- Modal for photo exif -->
            <photo-exif :photo="photo"></photo-exif>
          </div>
        </v-card>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import PhotoExif from './PhotoExif.vue';

export default {
  name: 'Photo',
  data: () => ({
    flipped: false,
    dialogDeletePhoto: false,
  }),
  props: ['photo'],
  components: {
    PhotoExif,
  },
  methods: {
    ...mapActions(['toggleLikePhoto']),
    handleDeletePhoto(photo) {
      this.$store.dispatch('deletePhoto', photo.id)
        .then(() => {
          this.$store.dispatch('notify', { text: `Photo "${photo.name}" has been deleted!`, color: 'warning' });
        })
        .catch((err) => {
          this.$store.dispatch('notify', { text: err, color: 'error' });
        });
      this.dialogDeletePhoto = false;
    },
  },

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

.flip-container {
  -webkit-perspective: 1000;
  -moz-perspective: 1000;
  -o-perspective: 1000;
  perspective: 1000;
  min-height: 120px;
}
.flipper {
  transform: perspective(1000px);
  -moz-transform: perspective(1000px);
  transform-style: preserve-3d;
  -moz-transform-style: preserve-3d;
  position: relative;
}
.front, .back {
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  -moz-backface-visibility: hidden;
  -o-backface-visibility: hidden;
  transition: 0.6s;
  -webkit-transition: 0.6s;
  -moz-transition: 0.6s;
  -o-transition: 0.6s;
  -ms-transition: 0.6s;
  transform-style: preserve-3d;
  -webkit-transform-style: preserve-3d;
  -moz-transform-style: preserve-3d;
  -o-transform-style: preserve-3d;
  -ms-transform-style: preserve-3d;
  top: 0;
  left: 0;
  width: 100%;
}
.back {
  transform: rotateY(-180deg);
  -webkit-transform: rotateY(-180deg);
  -moz-transform: rotateY(-180deg);
  -o-transform: rotateY(-180deg);
  -ms-transform: rotateY(-180deg);
  position: absolute;
}
.flip-container.flipped .back {
  transform: rotateY(0deg);
  -webkit-transform: rotateY(0deg);
  -moz-transform: rotateY(0deg);
  -o-transform: rotateY(0deg);
  -ms-transform: rotateY(0deg);
}
.flip-container.flipped .front {
  transform: rotateY(180deg);
  -webkit-transform: rotateY(180deg);
  -moz-transform: rotateY(180deg);
  -o-transform: rotateY(180deg);
  -ms-transform: rotateY(180deg);
}
.front {
  z-index: 2;
}
</style>
