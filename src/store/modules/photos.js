// import axios from 'axios';

const fakePhotos = [];
for (let i = 0; i < 25; i += 1) {
  fakePhotos.push({
    id: i,
    src: `https://picsum.photos/500/300?image=${i * 5 + 9}`,
    lazySrc: `https://picsum.photos/10/6?image=${i * 5 + 9}`,
    is_liked: false,
    name: `image ${i}`,
    date: 'March 31, 2019',
    time: '9h32',
    location: 'Paris, France',
    camera: 'Nexus 5, Android',
    lastModification: 'June 2, 2019',
    lastModificationTime: '6h33',
    tags: ['Dog', 'Holidays'],
  });
}

const state = {
  photos: fakePhotos,
};

const getters = {
  allPhotos: (state_) => state_.photos,
};

const actions = {
  async fetchTodos({ commit }) {
    const response = state.photos;
    commit('setTodos', response);
  },
};

const mutations = {
  setTodos: (state_, photos) => {
    const s = state_;
    s.photos = photos;
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
