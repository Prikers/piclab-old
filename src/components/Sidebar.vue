<template>
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

</template>

<script>
export default {
  name: 'Sidebar',
};
</script>
