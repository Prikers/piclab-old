<template>
  <v-app id="app" dark>

    <!-- SIDEBAR -->
    <v-navigation-drawer
      app
      clipped
      mini-variant
      id="sidebar"
    >
      <div class="d-flex flex-column justify-space-between fill-height">

        <v-list dense>
          <v-list-item link to="/dashboard">
            <v-list-item-action>
              <v-icon>mdi-view-dashboard</v-icon>
            </v-list-item-action>
            <v-list-item-content>Dashboard</v-list-item-content>
          </v-list-item>
          <v-list-item link to='/gallery'>
            <v-list-item-action>
              <v-icon>mdi-image-multiple</v-icon>
            </v-list-item-action>
            <v-list-item-content>Gallery</v-list-item-content>
          </v-list-item>
          <v-list-item link to='/face-identification'>
            <v-list-item-action>
              <v-icon>mdi-account-search</v-icon>
            </v-list-item-action>
            <v-list-item-content>Face Recognition</v-list-item-content>
          </v-list-item>
          <v-list-item link to="/deduplicator">
            <v-list-item-action>
              <v-icon>mdi-book-remove-multiple</v-icon>
            </v-list-item-action>
            <v-list-item-content>Deduplication</v-list-item-content>
          </v-list-item>
          <v-list-item link to="/smart-art">
            <v-list-item-action>
              <v-icon>mdi-image-frame</v-icon>
            </v-list-item-action>
            <v-list-item-content>Smart Art</v-list-item-content>
          </v-list-item>
        </v-list>

        <v-list dense>
          <v-list-item link to="/settings">
            <v-list-item-action>
              <v-icon>mdi-cog</v-icon>
            </v-list-item-action>
            <v-list-item-content></v-list-item-content>
          </v-list-item>
        </v-list>

      </div>

    </v-navigation-drawer>

    <!-- NAVBAR -->
    <v-app-bar app
      elevate-on-scroll
      clipped-left
      clipped-right
    >
      <router-link to="/">
        <img class="mr-3" :src="require('./assets/logo.svg')" height="30"/>
      </router-link>
      <v-toolbar-title class="primary--text display-1">Piclab</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn v-if="!isLoggedIn" text large to='/login'>
        <v-icon class='mr-2'>mdi-account-check</v-icon> Login
      </v-btn>
      <v-btn v-if="!isLoggedIn" text large to='/register'>
        <v-icon class='mr-2'>mdi-account-plus</v-icon> Register
      </v-btn>
      <v-btn v-else text large @click="logout">
        <v-icon class='mr-2'>mdi-account</v-icon> Logout
      </v-btn>

    </v-app-bar>

    <!-- MAIN CONTENT -->
    <v-content>
      <Notification />
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-content>

  </v-app>
</template>

<script>
import axios from 'axios';
import Notification from './components/Notification.vue';
import router from './router';
import store from './store';

export default {
  name: 'piclab',
  data: () => ({
  }),
  components: {
    Notification,
  },
  computed: {
    isLoggedIn() {
      return this.$store.getters.isLoggedIn;
    },
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
        .then(() => {
          this.$router.push('/');
        });
    },
  },
  created: () => {
    // Handle expired tokens by intercepting 401 api calls
    axios.interceptors.response.use(
      (response) => response, // Return a successful response back to the calling service
      (error) => {
        // 1. Return non authentication-related errors back to the calling service
        if (error.response.status !== 401) {
          return new Promise((resolve, reject) => {
            reject(error);
          });
        }
        // 2. Logout user if token refresh didn't work or user is disabled
        if (error.config.url.includes('/token/refresh/')) {
          store.dispatch('logout');
          router.push('/');
          return new Promise((resolve, reject) => {
            reject(error);
          });
        }

        // 3. Otherwise, try request again with new token
        return store.dispatch('refreshToken')
          .then(() => {
            // New request with new token
            const { config } = error;
            const token = localStorage.getItem('token');
            config.headers['Authorization'] = `Bearer ${token}`;

            return new Promise((resolve, reject) => {
              axios.request(config).then((response) => {
                resolve(response);
              }).catch((error_) => {
                reject(error_);
              });
            });
          })
          .catch((error_) => {
            throw error_;
          });
      },
    );
  },
};
</script>
