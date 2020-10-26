<template>
  <div class="wrapper">
    <v-container fluid>

      <h1>Dashboard</h1>

      <v-row>

        <create-project></create-project>

        <!-- Show a notification -->
        <v-btn
          color="teal"
          dark
          @click="showNotification"
          class="ma-4"
        >
          Show A Notification
        </v-btn>

        <!-- Button for testing purposes. TODO: delete -->
        <v-btn
          color="amber"
          dark
          @click="testStuff"
          class="ma-4"
        >
          Test A Request
        </v-btn>

      </v-row>

      <photo-file-upload></photo-file-upload>

    </v-container>
  </div>
</template>

<script>
import PhotoFileUpload from '../components/PhotoFileUpload.vue';
import CreateProject from '../components/CreateProject.vue';

export default {
  name: 'Dashboard',
  components: {
    PhotoFileUpload,
    CreateProject,
  },
  methods: {
    showNotification() {
      this.$store.dispatch('notify', {
        text: 'First Notification of the night',
        color: 'error',
        timeout: 3000,
      });
    },
    testStuff() {
      this.$store.dispatch('fetchUserProfile');
    },
  },
};
</script>
