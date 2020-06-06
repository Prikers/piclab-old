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
            <v-list-item-content>MELAINE</v-list-item-content>
          </v-list-item>
          <v-list-item link to='/gallery'>
            <v-list-item-action>
              <v-icon>mdi-image-multiple</v-icon>
            </v-list-item-action>
            <v-list-item-content></v-list-item-content>
          </v-list-item>
          <v-list-item link to='/face-identification'>
            <v-list-item-action>
              <v-icon>mdi-account-search</v-icon>
            </v-list-item-action>
            <v-list-item-content></v-list-item-content>
          </v-list-item>
          <v-list-item link to="/deduplicator">
            <v-list-item-action>
              <v-icon>mdi-book-remove-multiple</v-icon>
            </v-list-item-action>
            <v-list-item-content></v-list-item-content>
          </v-list-item>
          <v-list-item link to="/smart-art">
            <v-list-item-action>
              <v-icon>mdi-image-frame</v-icon>
            </v-list-item-action>
            <v-list-item-content></v-list-item-content>
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

      <v-btn icon>
        <v-icon>mdi-heart</v-icon>
      </v-btn>

      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>

    </v-app-bar>

    <!-- MAIN CONTENT -->
    <v-content>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-content>

  </v-app>
</template>


<script>
export default {
  name: 'piclab',
  data: () => ({
    //
  }),
};
</script>
