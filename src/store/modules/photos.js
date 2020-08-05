import axios from 'axios';

const state = {
  photos: [],
};

const getters = {
  allPhotos: (state) => state.photos,
};

const actions = {
  async fetchPhotos({ commit }) {
    const response = await axios.get(
      'http://127.0.0.1:8000/api/photos/',
    );
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
