const state = {
  notification: {},
};

const getters = {
  notification: (state) => state.notification,
};

const actions = {
  notify({ commit }, notification) {
    notification.showing = true;
    notification.color = notification.color || 'success';
    notification.timeout = notification.timeout || 5000;
    commit('setNotification', notification);
  },
};

const mutations = {
  setNotification: (state, notification) => {
    state.notification = notification;
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
