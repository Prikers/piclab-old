<template>
  <div class="wrapper">
    <v-container fluid>

      <h1>Dashboard</h1>

      <v-row>
        <!-- New Project Modal -->
        <v-dialog v-model="dialog" persistent max-width="600px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="indigo"
              dark
              v-bind="attrs"
              v-on="on"
              class="ma-4"
            >
              New Project
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">Create A New Project</span>
            </v-card-title>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12">
                    <v-text-field
                      label="Project Name"
                      v-model="projectName"
                      required
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" text @click="closeDialog">Close</v-btn>
              <v-btn color="primary" text @click="createProject">Save</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

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

    </v-container>
  </div>
</template>

<script>
// import axios from 'axios';

export default {
  name: 'Dashboard',

  data: () => ({
    dialog: false,
    projectName: '',
  }),

  methods: {
    showNotification() {
      this.$store.dispatch('notify', {
        text: 'First Notification of the night',
        color: 'error',
        timeout: 3000,
      });
    },

    closeDialog() {
      this.projectName = '';
      this.dialog = false;
    },

    createProject() {
      const name = this.projectName;
      this.$store.dispatch('createProject', name)
        .then(() => {
          this.$store.dispatch('notify', { text: `Project "${name}" successfully created!` });
        })
        .catch((err) => {
          this.$store.dispatch('notify', { text: err, color: 'error' });
        });
      this.projectName = '';
      this.dialog = false;
    },

    testStuff() {
      this.$store.dispatch('fetchUserProfile');
    },
  },
};
</script>
