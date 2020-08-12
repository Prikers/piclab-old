import axios from 'axios';

const REST_ENDPOINT = 'http://localhost:8000/';

const state = {
  status: '',
  token: localStorage.getItem('token') || '',
  refreshToken: localStorage.getItem('refreshToken') || '',
  user: {},
  error: '',
};

const getters = {
  isLoggedIn: (state) => !!state.token,
  authStatus: (state) => state.status,
  authErrors: (state) => state.error,
};

const actions = {

  login({ commit }, user) {
    return new Promise((resolve, reject) => {
      commit('login_request');
      axios.post(`${REST_ENDPOINT}api/token/`, user)
        .then((resp) => {
          const { refresh, access } = resp.data;
          localStorage.setItem('token', access);
          localStorage.setItem('refreshToken', refresh);
          axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
          commit('login_success', access, refresh, user);
          resolve(resp);
        })
        .catch((err) => {
          commit('login_error', err);
          localStorage.removeItem('token');
          localStorage.removeItem('refreshToken');
          axios.defaults.headers.common['Authorization'] = '';
          reject(err);
        });
    });
  },

  register({ commit }, user) {
    return new Promise((resolve, reject) => {
      commit('register_request');
      axios.post(`${REST_ENDPOINT}api/register/`, user)
        .then((resp) => {
          const createdUser = resp.data;
          commit('register_success', createdUser);
          resolve(resp);
        })
        .catch((err) => {
          commit('register_error', err);
          reject(err);
        });
    });
  },

  logout({ commit }) {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    axios.defaults.headers.common['Authorization'] = '';
    commit('logout');
  },

  refreshToken({ commit }) {
    return new Promise((resolve, reject) => {
      commit('refresh_request');
      axios.post(`${REST_ENDPOINT}api/token/refresh/`, { refresh: localStorage.getItem('refreshToken') })
        .then((resp) => {
          localStorage.setItem('token', resp.data.access);
          axios.defaults.headers.common['Authorization'] = `Bearer ${resp.data.access}`;
          commit('refresh_success', resp.data.access);
          resolve(resp);
        })
        .catch((err) => {
          commit('refresh_error', err);
          reject(err);
        });
    });
  },

};

const mutations = {
  register_request(state) {
    state.status = 'register_loading';
  },
  register_success(state, user) {
    state.status = 'registered';
    state.user = user;
  },
  register_error(state, error) {
    state.status = 'register_error';
    state.error = error;
  },
  login_request(state) {
    state.status = 'login_loading';
  },
  login_success(state, access, refresh, user) {
    state.status = 'login_success';
    state.token = access;
    state.refreshToken = refresh;
    state.user = user;
  },
  login_error(state, error) {
    state.status = 'login_error';
    state.error = error;
  },
  refresh_request(state) {
    state.status = 'refresh_loading';
  },
  refresh_success(state, access) {
    state.status = 'refresh_success';
    state.token = access;
  },
  refresh_error(state, error) {
    state.status = 'refresh_error';
    state.error = error;
  },
  logout(state) {
    state.status = '';
    state.token = '';
    state.refreshToken = '';
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
