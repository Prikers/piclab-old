<template>
  <v-dialog v-model="dialogUpload" max-width="600px">
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        v-bind="attrs"
        v-on="on"
        fab
        color="indigo"
        class="ma-3"
        dark
        fixed
        bottom
        right
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">Upload New Photos</span>
      </v-card-title>
      <v-card-text>
        <input
          type="file" id="photoFiles" ref="photoFilesInput" style="display: none"
          multiple
          @change="handlePhotoFilesSelected"
        />
        <v-btn
          @click="$refs.photoFilesInput.click()"
          min-height="100px"
          block
          outlined
          text
        >
          Browse
        </v-btn>

        <v-list dense>
          <v-list-item-group>
            <v-list-item v-for="(photoFile, i) in photoFiles" :key="i">
              <v-list-item-icon>
                <v-icon>mdi-image</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title v-text="photoFile.name"></v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>

      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" text @click="closeDialogUpload">Close</v-btn>
        <v-btn color="primary" text @click="uploadPhotoFile">Upload</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'PhotoFileUpload',

  data: () => ({
    photoFiles: [],
    dialogUpload: false,
  }),

  methods: {
    ...mapActions(['notify', 'uploadPhotos']),
    closeDialogUpload() {
      this.photoFiles = [];
      this.dialogUpload = false;
    },
    handlePhotoFilesSelected() {
      this.photoFiles = this.$refs.photoFilesInput.files;
    },
    uploadPhotoFile() {
      const formData = new FormData();
      this.photoFiles.forEach((file) => {
        formData.append('image', file);
      });
      this.uploadPhotos(formData)
        .then(() => {
          const verbose = (this.photoFiles.length > 1) ? 'photos' : 'photo';
          this.notify({ text: `${this.photoFiles.length} new ${verbose} successfully uploaded!` });
          this.closeDialogUpload();
        })
        .catch((err) => {
          this.notify({ text: err, color: 'error' });
        });
    },
  },
};
</script>
