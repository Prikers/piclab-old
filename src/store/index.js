import Vuex from 'vuex';
import Vue from 'vue';

import photos from './modules/photos';

// Load Vuex
Vue.use(Vuex);

// Create store
export default new Vuex.Store({
  modules: {
    photos,
  },
});
