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
      </v-row>

      <Deduplicator />

    </v-container>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import Deduplicator from '../components/Deduplicator.vue';

export default {
  name: 'Tweaks',
  components: {
    Deduplicator,
  },
  methods: {
    ...mapActions(['fetchDuplicates']),
  },
  computed: {
    ...mapGetters(['allDuplicates']),
  },
  created() {
    this.fetchDuplicates();
  },
};
</script>
