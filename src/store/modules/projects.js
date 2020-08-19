import axios from 'axios';

const REST_ENDPOINT = 'http://localhost:8000/';

const state = {
  projects: [],
  currentProject: '',
};

const getters = {
  allProjects: (state) => state.projects,
  currentProject: (state) => state.currentProject,
};

const actions = {
  async fetchProjects({ commit }) {
    const response = await axios.get(`${REST_ENDPOINT}api/projects/`);
    commit('setProjects', response.data);
  },
  async createProject({ commit }, projectName) {
    const response = await axios.post(`${REST_ENDPOINT}api/projects/`, { name: projectName });
    commit('addProject', response.data);
  },
  setCurrentProject({ commit }, project) {
    commit('setCurrentProject', project);
  },
  clearProjects({ commit }) {
    commit('clearProjects');
  },
};

const mutations = {
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
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
