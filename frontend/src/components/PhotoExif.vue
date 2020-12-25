<template>
  <div class="text-center">
    <v-dialog
      v-model="dialog"
      width="500"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn text v-bind="attrs" v-on="on">
          More info
        </v-btn>
      </template>

      <v-card>
        <v-card-title>
          {{ photo.name }}
        </v-card-title>
        <v-card-text>
          <v-simple-table dense fixed-header>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">Name</th>
                  <th class="text-left">Info</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(value, key, index) in photo.exif"
                  :key="index"
                >
                  <td>{{ key }}</td>
                  <td>{{ value }}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="dialog = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: 'PhotoExif',
  data: () => ({
    dialog: false,
  }),
  props: ['photo'],
};
</script>
