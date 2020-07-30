import Vue from 'vue';
import VueRouter from 'vue-router';

import Dashboard from '../views/Dashboard.vue';
import Deduplicator from '../views/Deduplicator.vue';
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
    path: '/deduplicator',
    name: 'deduplicator',
    component: Deduplicator,
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
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
