import axios from 'axios';

const state = {
  status: '',
  token: localStorage.getItem('token') || '',
  refresh_token: localStorage.getItem('refresh_token') || '',
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
      axios.post('http://localhost:8000/api/token/', user)
        .then((resp) => {
          const { refresh, access } = resp.data;
          localStorage.setItem('token', access);
          localStorage.setItem('refresh_token', refresh);
          axios.defaults.headers.common.Authorization = access;
          commit('login_success', access, refresh, user);
          resolve(resp);
        })
        .catch((err) => {
          commit('login_error', err);
          localStorage.removeItem('token');
          localStorage.removeItem('refresh_token');
          reject(err);
        });
    });
    // TODO alert user for correct login
  },

  register({ commit }, user) {
    return new Promise((resolve, reject) => {
      commit('register_request');
      axios.post('http://localhost:8000/api/register/', user)
        .then((resp) => {
          const createdUser = resp.data;
          commit('register_success', createdUser);
          resolve(resp);
        })
        .catch((err) => {
          commit('register_error', err);
          reject(err);
        });
      // TODO alert user that account has been created
    });
  },

  logout({ commit }) {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
    commit('logout');
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
    state.refresh_token = refresh;
    state.user = user;
  },
  login_error(state, error) {
    state.status = 'login_error';
    state.error = error;
  },
  logout(state) {
    state.status = '';
    state.token = '';
    state.refresh_token = '';
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
