<template>
  <div class="wrapper">
    <Photos/>
  </div>
</template>

<script>
import Photos from "@/components/Photos.vue"; // @ is an alias to /src
import { mapGetters } from "vuex";

export default {
  name: 'Gallery',
  components: {
    Photos,
  },
};
</script>
