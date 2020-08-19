<template>
  <v-app id="app" dark>

    <!-- SIDEBAR -->
    <Sidebar />

    <!-- NAVBAR -->
    <Navbar />

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
import Navbar from './components/Navbar.vue';
import router from './router';
import Sidebar from './components/Sidebar.vue';
import store from './store';

export default {
  name: 'piclab',
  data: () => ({
  }),
  components: {
    Navbar,
    Notification,
    Sidebar,
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
