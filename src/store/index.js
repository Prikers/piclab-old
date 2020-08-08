import Vuex from 'vuex';
import Vue from 'vue';

import auth from './modules/auth';
import notifications from './modules/notifications';
import photos from './modules/photos';

// Load Vuex
Vue.use(Vuex);

// Create store
export default new Vuex.Store({
  modules: {
    auth,
    notifications,
    photos,
  },
});
