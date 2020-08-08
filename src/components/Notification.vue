<template>
  <v-snackbar
    v-model="notification.showing"
    :timeout="notification.timeout"
    :color="notification.color"
  >
    {{ notification.text }}
    <template>
      <v-btn
        text
        @click="notification.showing = false"
      >
        Close
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'Notification',
  computed: {
    ...mapGetters(['notification']),
  },
};
</script>

<style>

</style>
