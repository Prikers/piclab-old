import axios from 'axios';

const REST_ENDPOINT = 'http://localhost:8000/';

const state = {
  photos: [],
};

const getters = {
  allPhotos: (state) => state.photos,
};

const actions = {
  async fetchPhotos({ commit }) {
    console.log(axios.defaults.headers.common);
    const response = await axios.get(`${REST_ENDPOINT}api/photos/`);
    commit('setPhotos', response.data);
  },
};

const mutations = {
  setPhotos: (state, photos) => {
    state.photos = photos;
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
