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
  async toggleLikePhoto({ commit, rootState }, photo) {
    const like = !photo.is_liked;
    const { currentProject } = rootState.profiles;
    const response = await axios.patch(
      `${REST_ENDPOINT}api/photos/${photo.id}/`,
      { is_liked: like },
      { params: { project: currentProject.id } },
    );
    commit('likePhoto', response.data);
  },
};

const mutations = {
  setPhotos: (state, photos) => {
    state.photos = photos;
  },
  likePhoto: (state, photo) => {
    state.photos = [...state.photos.map((p) => (p.id !== photo.id ? p : photo))];
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
