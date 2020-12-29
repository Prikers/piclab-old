module.exports = {
  env: {
    browser: true,
    es6: true,
  },
  extends: [
    'plugin:vue/essential',
    'airbnb-base',
  ],
  globals: {
    Atomics: 'readonly',
    SharedArrayBuffer: 'readonly',
  },
  parserOptions: {
    ecmaVersion: 2018,
    sourceType: 'module',
  },
  plugins: [
    'vue',
  ],
  rules: {
    'dot-notation': 0,
    // 'no-param-reassign': [2, {'props': false}],
    'no-param-reassign' : [
      'error',
      {
        'props': true,
        'ignorePropertyModificationsFor': [
          'state',
          'notification',
          'photo',
        ]
      }
    ],
    'no-shadow': ['error', {'allow': ['state', 'user']}]
  },
};
