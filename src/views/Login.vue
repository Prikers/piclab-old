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
            <v-toolbar-title>Login to Piclab</v-toolbar-title>
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
              :disabled="!valid"
              @click="validate"
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
    valid: true,
    username: '',
    password: '',
    showPassword: false,
    rules: {
      required: (v) => !!v || 'This field is required',
      minPassword: (v) => v.length >= 8 || 'The password should be at least 8 characters',
      minUsername: (v) => v.length >= 3 || 'The username should be at least 3 characters',
      maxUsername: (v) => v.length < 20 || 'The username should be less than 20 characters',
    },
  }),
  methods: {
    validate() {
      this.$refs.form.validate();
    },
  },
};
</script>
