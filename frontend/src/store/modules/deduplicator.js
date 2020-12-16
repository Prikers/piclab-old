import axios from 'axios';
import api from './api';

const { API_URL } = api;

const state = {
  duplicates: [],
};

const getters = {
  allDuplicates: (state) => state.duplicates,
};

const actions = {
  async fetchDuplicates({ commit, rootState }) {
    const { currentProject } = rootState.profiles;
    const params = new URLSearchParams(); // Required because of duplicated 'status' param
    params.append('project', currentProject.id);
    params.append('is_duplicated', true);
    params.append('status', 1);
    params.append('status', 3);
    const response = await axios.get(`${API_URL}/hash/`, { params });
    // Order duplicates with 'todo' first
    const data = response.data
      .filter((dup) => dup.status === 'todo')
      .concat(response.data.filter((dup) => dup.status !== 'todo'));
    // Duplicates are all contained in a single array - Let's unflatten it!
    const duplicates = {};
    data.forEach((dup) => {
      if (!(dup.duplicate_id in duplicates)) {
        duplicates[dup.duplicate_id] = [dup];
      } else {
        duplicates[dup.duplicate_id].push(dup);
      }
    });
    commit('setDuplicates', duplicates);
  },

  async markPhotoAsReviewed({ commit, rootState }, { hash, review }) {
    const { currentProject } = rootState.profiles;
    const reviews = { done: 2, skipped: 3 };
    const datetime = new Date();
    await axios.patch(
      `${API_URL}/hash/${hash.id}/`,
      { status: reviews[review], date_status: datetime.toISOString() },
      { params: { project: currentProject.id } },
    );
    commit('markPhotoAsReviewed', hash, reviews[review], datetime);
  },
};

const mutations = {
  setDuplicates: (state, duplicates) => {
    state.duplicates = duplicates;
  },
  markPhotoAsReviewed: (state, hash, status, datetime) => {
    const index = state.duplicates[hash.duplicate_id].findIndex((h) => h.id === hash.id);
    state.duplicates[hash.duplicate_id][index].status = status;
    state.duplicates[hash.duplicate_id][index].date_status = datetime;
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
