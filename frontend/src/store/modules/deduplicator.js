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
    const response = await axios.get(`${API_URL}/hash/`, {
      params: {
        project: currentProject.id,
        is_duplicated: true,
      },
    });
    // Duplicates are all contained in a single array - Let's unflatten it!
    const duplicates = {};
    response.data.forEach((dup) => {
      if (!(dup.duplicate_id in duplicates)) {
        duplicates[dup.duplicate_id] = [dup];
      } else {
        duplicates[dup.duplicate_id].push(dup);
      }
    });
    commit('setDuplicates', duplicates);
  },
};

const mutations = {
  setDuplicates: (state, duplicates) => {
    state.duplicates = duplicates;
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
