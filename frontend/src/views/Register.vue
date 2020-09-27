<template>
  <v-container class="fill-height" fluid >
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar
            color="primary"
            dark
            flat
          >
            <v-toolbar-title>Register to Piclab</v-toolbar-title>
          </v-toolbar>

          <v-card-text>
            <v-form
              ref="form"
              v-model="valid"
            >
              <v-text-field
                v-model="username"
                label="Username"
                prepend-icon="mdi-account"
                type="text"
                :rules="[rules.required, rules.minUsername, rules.maxUsername]"
                hint="Between 3 and 20 characters"
              ></v-text-field>
              <v-text-field
                v-model="email"
                label="Email"
                prepend-icon="mdi-email"
                type="email"
                :rules="[rules.required, rules.email]"
              ></v-text-field>
              <v-text-field
                v-model="password1"
                label="Password"
                prepend-icon="mdi-lock"
                :append-icon="showPassword1 ? 'mdi-eye' : 'mdi-eye-off'"
                :rules="[rules.required, rules.minPassword]"
                :type="showPassword1 ? 'text' : 'password'"
                counter
                hint="At least 8 characters"
                @click:append="showPassword1 = !showPassword1"
              ></v-text-field>
              <v-text-field
                v-model="password2"
                label="Password Confirmation"
                prepend-icon="mdi-lock-check"
                :append-icon="showPassword2 ? 'mdi-eye' : 'mdi-eye-off'"
                :rules="[rules.required, rules.minPassword, passwordConfirmationRule]"
                :type="showPassword2 ? 'text' : 'password'"
                counter
                hint="At least 8 characters"
                @click:append="showPassword2 = !showPassword2"
              ></v-text-field>
            </v-form>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              :disabled="!valid"
              @click="register"
            >
              Register
            </v-btn>
          </v-card-actions>

        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'Register',
  data: () => ({
    valid: true,
    username: '',
    email: '',
    password1: '',
    password2: '',
    showPassword1: false,
    showPassword2: false,
    rules: {
      required: (v) => !!v || 'This field is required',
      minPassword: (v) => v.length >= 8 || 'The password should be at least 8 characters',
      minUsername: (v) => v.length >= 3 || 'The username should be at least 3 characters',
      maxUsername: (v) => v.length < 20 || 'The username should be less than 20 characters',
      email: (v) => !v || /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail must be valid',
    },
  }),
  methods: {
    register() {
      this.$refs.form.validate();
      const data = {
        email: this.email,
        username: this.username,
        password: this.password1,
        password_confirm: this.password2,
      };
      this.$store.dispatch('register', data)
        .then(() => {
          this.$store.dispatch('notify', { text: 'Your account has been successfully created!' });
          this.$router.push('/login');
        })
        .catch((err) => {
          const errors = err.response.data;
          if (errors) {
            Object.values(errors).forEach((error) => {
              error.forEach((detail) => this.$store.dispatch('notify', { text: detail, color: 'error' }));
            });
          } else {
            this.$store.dispatch('notify', { text: err, color: 'error' });
          }
        });
    },
  },
  computed: {
    passwordConfirmationRule() {
      return this.password1 === this.password2 || 'Passwords must match';
    },
  },
};
</script>
