import Vuex from 'vuex';
import Vue from 'vue';

import photos from './modules/photos';
import auth from './modules/auth';

// Load Vuex
Vue.use(Vuex);

// Create store
export default new Vuex.Store({
  modules: {
    photos,
    auth,
  },
});
