<template>
  <div v-bind:class="flipped ? 'flip-container flipped': 'flip-container'">
    <div class="flipper">
      <div class="front">
        <v-hover v-slot:default="{ hover }">
          <v-card
            :elevation="hover ? 12 : 2"
            :class="{ 'on-hover': hover }"
          >
            <v-img
              :src="photo.image"
              aspect-ratio="1"
              class="d-flex flex-row align-end"
            >
                <div class="d-flex flow-column">
                  <v-btn
                    @click="togglePhotoDetails(photo)"
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
          <v-card
            elevation="12"
            height="100%"
            class="d-flex flex-column"
          >
            <v-list dense class="ml-4">
              <v-subheader>{{photo.name}}</v-subheader>
              <v-list-item>
                <v-list-item-icon>
                  <v-icon>mdi-calendar</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>2020, Feb 17th</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-icon>
                  <v-icon>mdi-clock</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>19h13 14s</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-icon>
                  <v-icon>mdi-pin</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>Paris, France</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list>
            <v-spacer></v-spacer>
            <v-btn icon @click="flipped=false">
              <v-icon>
                mdi-arrow-left
              </v-icon>
            </v-btn>
          </v-card>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'Photo',
  data: () => ({
    flipped: false,
  }),
  props: ['photo'],
  methods: {
    ...mapActions(['toggleLikePhoto']),
    togglePhotoDetails(photo) {
      this.flipped = true;
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
}
.flip-container {
  min-height: 120px;
}
.flipper {
  -moz-transform: perspective(1000px);
  -moz-transform-style: preserve-3d;
  position: relative;
}
.front,
.back {
  -webkit-backface-visibility: hidden;
  -moz-backface-visibility: hidden;
  -o-backface-visibility: hidden;
  backface-visibility: hidden;
  -webkit-transition: 0.6s;
  -webkit-transform-style: preserve-3d;
  -moz-transition: 0.6s;
  -moz-transform-style: preserve-3d;
  -o-transition: 0.6s;
  -o-transform-style: preserve-3d;
  -ms-transition: 0.6s;
  -ms-transform-style: preserve-3d;
  transition: 0.6s;
  transform-style: preserve-3d;
  top: 0;
  left: 0;
  width: 100%;
}
.back {
  -webkit-transform: rotateY(-180deg);
  -moz-transform: rotateY(-180deg);
  -o-transform: rotateY(-180deg);
  -ms-transform: rotateY(-180deg);
  transform: rotateY(-180deg);
  position: absolute;
}
.flip-container.flipped .back {
  -webkit-transform: rotateY(0deg);
  -moz-transform: rotateY(0deg);
  -o-transform: rotateY(0deg);
  -ms-transform: rotateY(0deg);
  transform: rotateY(0deg);
}
.flip-container.flipped .front {
  -webkit-transform: rotateY(180deg);
  -moz-transform: rotateY(180deg);
  -o-transform: rotateY(180deg);
  -ms-transform: rotateY(180deg);
  transform: rotateY(180deg);
}
.front {
  z-index: 2;
}

</style>
