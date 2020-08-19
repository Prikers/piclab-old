<template>
  <v-app-bar app
    elevate-on-scroll
    clipped-left
    clipped-right
  >
    <router-link to="/">
      <img class="mr-3" :src="require('../assets/logo.svg')" height="30"/>
    </router-link>
    <v-toolbar-title class="primary--text display-1">Piclab</v-toolbar-title>

    <v-spacer></v-spacer>

    <v-menu
      v-if="isLoggedIn"
      offset-y
      :nudge-width="200"
      :close-on-content-click="false"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          icon
          v-bind="attrs"
          v-on="on"
        >
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
      </template>
      <v-card>
        <v-list>
          <!-- PROFILE -->
          <v-list-item>
            <v-list-item-action>
              <v-icon class='mr-2'>mdi-account-edit</v-icon>
            </v-list-item-action>
            <v-list-item-title>My Profile</v-list-item-title>
          </v-list-item>

          <!-- PROJECT -->
          <v-menu open-on-hover offset-x left>
            <template v-slot:activator="{ on, attrs }">
              <v-list-item
                v-bind="attrs"
                v-on="on"
              >
                <v-list-item-action>
                  <v-icon class='mr-2'>mdi-folder-multiple</v-icon>
                </v-list-item-action>
                <v-list-item-title>Switch Project</v-list-item-title>
              </v-list-item>
            </template>
            <v-list>
              <v-list-item
                v-for="(project, index) in allProjects"
                :key="index"
                @click="setCurrentProject(project)"
              >
                <v-list-item-title>{{ project.name }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>

          <v-divider></v-divider>

          <v-list-item @click="logout">
            <v-list-item-action>
              <v-icon class='mr-2'>mdi-account-lock</v-icon>
            </v-list-item-action>
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-card>
    </v-menu>

    <v-btn v-if="!isLoggedIn" text large to='/login'>
      <v-icon class='mr-2'>mdi-account-check</v-icon> Login
    </v-btn>
    <v-btn v-if="!isLoggedIn" text large to='/register'>
      <v-icon class='mr-2'>mdi-account-plus</v-icon> Register
    </v-btn>

  </v-app-bar>

</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'Navbar',
  computed: {
    isLoggedIn() {
      return this.$store.getters.isLoggedIn;
    },
    ...mapGetters(['allProjects']),
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
        .then(() => {
          this.$router.push('/');
        });
    },
    ...mapActions(['fetchProjects', 'setCurrentProject']),
  },
  created() {
    this.fetchProjects();
  },
};
</script>
