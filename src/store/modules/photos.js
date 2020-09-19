import axios from 'axios';

const REST_ENDPOINT = 'http://localhost:8000/';

const state = {
  photos: [],
};

const getters = {
  allPhotos: (state) => state.photos,
};

const actions = {
  async fetchPhotos({ commit, rootState }) {
    const { currentProject } = rootState.profiles;
    const response = await axios.get(`${REST_ENDPOINT}api/photos/`, {
      params: {
        project: currentProject.id,
      },
    });
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
