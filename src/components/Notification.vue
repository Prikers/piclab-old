<template>
  <div>
    <v-snackbar
      v-for="(notification, index) in notifications"
      :key=index
      v-model="notification.showing"
      :timeout="notification.timeout"
      :color="notification.color"
      :style="`bottom: ${(index * 60) + 8}px`"
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
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'Notification',
  computed: {
    ...mapGetters(['notifications']),
  },
};
</script>

<style>

</style>
