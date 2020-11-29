<template>
  <div class="wrapper">
    <v-container fluid>
      <!-- KPI ROW -->
      <v-row>
        <v-col cols="3">
          <v-card
            class="mx-auto"
            dark
            color="secondary"
          >
            <v-card-title>
              <v-icon left>mdi-account-box-multiple-outline</v-icon>
              <span class="title font-weight-light">Identified Duplicates</span>
            </v-card-title>
            <v-card-text class="headline font-weight-bold text-center">
              {{ Object.keys(this.allDuplicates).length }}
            </v-card-text>
          </v-card>
        </v-col>
        <v-btn @click="nextDuplicate">
          Next Duplicate
        </v-btn>
      </v-row>
      <!-- PHOTO ROW -->
      <v-row>
        <v-col
          v-for="(duplicate, index) in allDuplicates[this.currentID]"
          :key="duplicate.id"
          class="d-flex child-flex flex-column"
          :cols=3
        >
          <Photo :photo="duplicate.photo" />
          <v-switch
            v-model="switches[index]"
            label="Delete"
            color="error"
          ></v-switch>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import Photo from '../components/Photo.vue';

export default {
  name: 'Deduplicator',
  data: () => ({
    currentID: '',
    allIDs: '',
    switches: [],
  }),
  components: {
    Photo,
  },
  methods: {
    ...mapActions(['fetchDuplicates']),
    nextDuplicate() {
      // Mark current Dup ID as done

      // Move to the next one
      const next = this.allIDs.indexOf(this.currentID) + 1;
      this.currentID = this.allIDs[next];
      this.switches = [];
      for (let i = 0; i < this.allDuplicates[this.currentID].length; i += 1) {
        this.switches[i] = false;
      }
    },
  },
  computed: {
    ...mapGetters(['allDuplicates']),
  },
  created() {
    this.fetchDuplicates();
    this.allIDs = Object.keys(this.allDuplicates);
    [this.currentID] = this.allIDs;
    for (let i = 0; i < this.allDuplicates[this.currentID].length; i += 1) {
      this.switches[i] = false;
    }
  },
};
</script>
