<template>
  <v-container class="fill-height" fluid >
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12" v-on:keyup.enter="login">
          <v-toolbar
            color="primary"
            dark
            flat
          >
            <v-toolbar-title>Login to Piclab</v-toolbar-title>
          </v-toolbar>

          <v-card-text>
            <v-form
              ref="form"
              v-model="valid"
            >
              <v-text-field
                v-model="email"
                label="Email"
                prepend-icon="mdi-email"
                type="email"
                :rules="[rules.required, rules.email]"
              ></v-text-field>
              <v-text-field
                v-model="password"
                label="Password"
                prepend-icon="mdi-lock"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :rules="[rules.required, rules.minPassword]"
                :type="showPassword ? 'text' : 'password'"
                counter
                hint="At least 8 characters"
                @click:append="showPassword = !showPassword"
              ></v-text-field>
            </v-form>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              :loading="loading"
              :disabled="!valid || loading"
              @click="login"
            >
              Login
            </v-btn>
          </v-card-actions>

        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'Login',
  data: () => ({
    email: '',
    password: '',
    valid: true,
    showPassword: false,
    rules: {
      required: (v) => !!v || 'This field is required',
      minPassword: (v) => v.length >= 8 || 'The password should be at least 8 characters',
      email: (v) => !v || /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail must be valid',
    },
    loading: false,
  }),
  methods: {
    login() {
      this.$refs.form.validate();
      const data = {
        email: this.email,
        password: this.password,
      };
      this.loading = true;
      this.$store.dispatch('login', data)
        .then(() => {
          this.$store.dispatch('notify', { text: 'Successfull Login. Welcome back!' });
          this.$router.push(this.$route.query.redirect || '/dashboard');
        })
        .catch((err) => {
          const text = err.response.status === 400 ? 'Incorrect email/password combination. Please try again.' : err;
          this.$store.dispatch('notify', { text, color: 'error' });
        });
      this.loading = false;
    },
  },
};
</script>
