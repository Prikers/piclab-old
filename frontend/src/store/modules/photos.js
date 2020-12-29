import axios from 'axios';
import api from './api';
import utils from './utils';

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

  async deletePhoto({ commit, rootState }, photoID) {
    const { currentProject } = rootState.profiles;
    await axios.delete(
      `${API_URL}/photos/${photoID}/`,
      { params: { project: currentProject.id } },
    );
    commit('deletePhoto', photoID);
  },
};

const mutations = {
  setPhotos: (state, photos) => {
    photos.forEach((photo) => {
      photo.datetime_photo = {
        exists: !!photo.datetime_photo,
        date: photo.datetime_photo ? new Date(photo.datetime_photo).toDateString() : 'Not defined',
        time: photo.datetime_photo ? new Date(photo.datetime_photo).toTimeString().substring(0, 8) : 'Not defined',
      };
      photo.file_size_hr = utils.humanReadableSize(photo.file_size);
      photo.camera = photo.camera ? photo.camera : 'Not defined';
    });
    state.photos = photos;
  },
  likePhoto: (state, photo) => {
    const index = state.photos.findIndex((p) => p.id === photo.id);
    state.photos[index].is_liked = photo.is_liked;
  },
  addPhotos: (state, newPhotos) => {
    state.photos = state.photos.concat(newPhotos);
  },
  deletePhoto: (state, photoID) => {
    state.photos = state.photos.filter((photo) => photo.id !== photoID);
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
