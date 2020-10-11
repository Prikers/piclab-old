import axios from 'axios';
import api from './api';

const { API_URL } = api;

const state = {
  photos: [],
};

const getters = {
  allPhotos: (state) => state.photos,
};

const actions = {
  async fetchPhotos({ commit, rootState }) {
    const { currentProject } = rootState.profiles;
    const response = await axios.get(`${API_URL}/photos/`, {
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
      `${API_URL}/photos/${photo.id}/`,
      { is_liked: like },
      { params: { project: currentProject.id } },
    );
    commit('likePhoto', response.data);
  },

  async uploadPhotos({ commit, rootState }, formData) {
    formData.append('project', rootState.profiles.currentProject.id);
    const response = await axios.post(
      `${API_URL}/photos/`,
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } },
    );
    commit('addPhotos', response.data);
  },
};

const mutations = {
  setPhotos: (state, photos) => {
    state.photos = photos;
  },
  likePhoto: (state, photo) => {
    const index = state.photos.findIndex((p) => p.id === photo.id);
    state.photos[index].is_liked = photo.is_liked;
  },
  addPhotos: (state, newPhotos) => {
    state.photos = state.photos.concat(newPhotos);
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
