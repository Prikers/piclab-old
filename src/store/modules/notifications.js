const state = {
  notifications: [],
};

const getters = {
  notifications: (state) => state.notifications,
};

const actions = {
  notify({ commit }, notification) {
    notification.showing = true;
    notification.color = notification.color || 'success';
    notification.timeout = (notification.timeout === undefined) ? 5000 : notification.timeout;
    commit('setNotification', notification);
  },
};

const mutations = {
  setNotification: (state, notification) => {
    state.notifications = state.notifications.filter((n) => n.showing).concat(notification);
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
