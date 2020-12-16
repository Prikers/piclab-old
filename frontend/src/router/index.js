import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '../store';

import Dashboard from '../views/Dashboard.vue';
import Tweaks from '../views/Tweaks.vue';
import FaceIdentification from '../views/FaceIdentification.vue';
import Gallery from '../views/Gallery.vue';
import LandingPage from '../views/LandingPage.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Settings from '../views/Settings.vue';
import SmartArt from '../views/SmartArt.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'landing-page',
    component: LandingPage,
    meta: {
      allowAnonymous: true,
    },
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
  },
  {
    path: '/gallery',
    name: 'gallery',
    component: Gallery,
  },
  {
    path: '/face-identification',
    name: 'face-identification',
    component: FaceIdentification,
  },
  {
    path: '/tweaks',
    name: 'tweaks',
    component: Tweaks,
  },
  {
    path: '/smart-art',
    name: 'smart-art',
    component: SmartArt,
  },
  {
    path: '/settings',
    name: 'settings',
    component: Settings,
  },
  {
    path: '/register',
    name: 'register',
    component: Register,
    meta: {
      allowAnonymous: true,
    },
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: {
      allowAnonymous: true,
    },
  },
];

const router = new VueRouter({
  routes,
});

router.beforeEach((to, from, next) => {
  if (!to.meta.allowAnonymous && !store.getters.isLoggedIn) {
    next({
      path: '/login',
      query: { redirect: to.fullPath },
    });
  } else {
    next();
  }
});

export default router;
