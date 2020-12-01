<template>
  <v-row justify="center">
    <v-dialog
      v-model="dialogDeduplicator"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="primary"
          v-bind="attrs"
          v-on="on"
        >
          Start Deduplication
        </v-btn>
      </template>
      <v-card>
        <v-toolbar
          dark
          color="primary"
        >
          <v-btn icon @click="dialogDeduplicator = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Deduplications</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn text>
              Save & Close
            </v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <v-row class="mx-auto mt-6 d-flex justify-center">
          <v-col
            v-for="(duplicate, index) in allDuplicates[this.currentID]"
            :key="duplicate.id"
            class="d-flex child-flex flex-column"
            :cols=3
          >
            <Photo :photo="duplicate.photo" />
            <v-switch
              v-model="switches[index]"
              :label="switches[index] ? 'Delete' : 'Keep'"
              color="error"
            ></v-switch>
          </v-col>
        </v-row>
        <v-row class="mx-auto d-flex justify-center">
          <v-col class="d-flex justify-center">
            <v-btn
              large
              class="mr-3"
              min-width=150
              color="secondary"
            >
              Review Later
            </v-btn>
            <v-btn
              large
              class="ml-3"
              min-width=150
              :color="switches.some(x => x) ? 'error' : 'primary'"
            >
              Save
            </v-btn>
          </v-col>
        </v-row>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import Photo from './Photo.vue';

export default {
  name: 'Deduplicator',
  components: {
    Photo,
  },
  data: () => ({
    dialogDeduplicator: false,
    currentID: '',
    allIDs: [],
    switches: [],
  }),
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
  async created() {
    await this.fetchDuplicates();
    console.log(this.allDuplicates);
    this.allIDs = Object.keys(this.allDuplicates);
    [this.currentID] = this.allIDs;
    for (let i = 0; i < this.allDuplicates[this.currentID].length; i += 1) {
      this.switches[i] = false;
    }
  },
};
</script>
