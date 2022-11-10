<script lang="ts">
  export let cloudName = "";
  export let uploadPreset = "";

  let files: any;

  // https://cloudinary.com/documentation/upload_images#code_explorer_upload_multiple_files_using_a_form_unsigned
  async function upload(cloudName: string, uploadPreset: string, file: any) {
    const formData = new FormData();
    formData.append("upload_preset", uploadPreset);
    formData.append("file", file);
    return await fetch(
      `https://api.cloudinary.com/v1_1/${cloudName}/image/upload`,
      {
        method: "POST",
        body: formData,
      }
    );
  }
  async function handleOnSubmit() {
    const response = await upload(cloudName, uploadPreset, files[0]);
  }
</script>

<form on:submit|preventDefault={handleOnSubmit}>
  <input bind:files type="file" />
  <input type="submit" />
</form>
