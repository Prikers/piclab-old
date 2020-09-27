import Vue from 'vue';
import Vuetify from 'vuetify/lib';
// import '@mdi/font/css/materialdesignicons.css'
// import 'material-design-icons-iconfont/dist/material-design-icons.css'

Vue.use(Vuetify);

const opts = {
  icons: {
    iconfont: 'mdi',
  },
  theme: {
    dark: true,
    themes: {
      dark: {
        // primary: '#1EB980',
        // secondary: '#045D56',
        // tertiary: '#FF6859',
        // quaternary: '#FFCF44',
        // quinary: '#B15DFF',
        // senary: '#72DEFF',
        // accent: '#82B1FF',
        // error: '#FF5252',
        // info: '#2196F3',
        // success: '#4CAF50',
        // warning: '#FFC107',
      },
    },
  },
};

export default new Vuetify(opts);
