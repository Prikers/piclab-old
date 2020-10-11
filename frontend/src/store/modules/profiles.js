import axios from 'axios';
import api from './api';

const { API_URL } = api;

const state = {
  projects: [],
  currentProject: {},
  profile: {},
};

const getters = {
  allProjects: (state) => state.projects,
  currentProject: (state) => state.currentProject,
};

const actions = {
  async fetchUserProfile({ commit }) {
    const response = await axios.get(`${API_URL}/profile/`);
    const profile = response.data[0];
    const currentProject = profile.projects.filter((p) => p.id === profile.current_project)[0];
    commit('setCurrentProject', currentProject);
    commit('setProjects', profile.projects);
    commit('setProfile', profile);
  },
  async createProject({ commit }, projectName) {
    const response = await axios.post(
      `${API_URL}/projects/`,
      { name: projectName },
    );
    commit('addProject', response.data);
    commit('setCurrentProject', response.data);
  },
  async setCurrentProject({ commit, state }, project) {
    const response = await axios.put(
      `${API_URL}/profile/${state.profile.id}/`,
      { current_project: project.id },
    );
    commit(
      'setCurrentProject',
      response.data.projects.filter((p) => p.id === response.data.current_project)[0],
    );
  },
  clearProjects({ commit }) {
    commit('clearProjects');
  },
};

const mutations = {
  setProfile: (state, profile) => {
    state.profile = profile;
  },
  setProjects: (state, projects) => {
    state.projects = projects;
  },
  setCurrentProject: (state, project) => {
    state.currentProject = project;
  },
  addProject: (state, project) => {
    state.projects.push(project);
  },
  clearProjects: (state) => {
    state.projects = [];
    state.currentProject = {};
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
