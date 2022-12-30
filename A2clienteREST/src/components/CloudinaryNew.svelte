<script lang="ts">
  export let cloudName = "";
  export let uploadPreset = "";

  let files: any;
  let title = "";
  let description = "";
  let street = "";
  let number = "";
  let city = "";
  let province = "";
  let cp = "";
  let country = "";
  let price = 0;
  let loading: boolean = false;
  let publishProgress = 0;

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
    loading = true;
    let image: string[] = [];
    if (files) {
      //image = await upload(cloudName, uploadPreset, files[0]).then(x => x.json()).then(x => [x.url]);
      //image = await Promise.all(files.map((fich : any) => upload(cloudName, uploadPreset, fich).then(x => x.json()).then(x => x.url)));
      for (let i = 0; i < files.length; i++) {
        let fich = files[i];
        let res = await upload(cloudName, uploadPreset, fich)
          .then((x) => x.json())
          .then((x) => x.url);
        image.push(res);
        publishProgress = ((i + 1) * 100) / (files.length);
        console.log(publishProgress);
      }
    } else {
      image = [];
    }
    const res = await fetch("/houses/new/newHandler", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title,
        description,
        street,
        number,
        city,
        province,
        cp,
        country,
        price,
        image,
      }),
    }).then((x) => {
      loading = false;
      return x.json();
    });
    window.location.href = res.redirect;
  }
</script>

<!--<form action="/houses/new/newHandler" method="post">-->
<form on:submit|preventDefault={handleOnSubmit}>
  <!-- <input hidden value="EXAMPLE_USER_HARDCODED" name="userId" /> TODO -->
  <div class="mb-3">
    <label for="title" class="form-label">Title</label>
    <input
      bind:value={title}
      type="text"
      name="title"
      class="form-control"
      id="title"
      aria-describedby="titleHelp"
      required
    />
  </div>
  <div class="mb-3">
    <label for="description" class="form-label">Description</label>
    <textarea
      bind:value={description}
      name="description"
      class="form-control"
      id="description"
    />
  </div>
  <div class="mb-3 row">
    <div class="col">
      <label for="street" class="form-label">Street</label>
      <input
        bind:value={street}
        type="text"
        name="street"
        class="form-control"
        id="street"
        required
      />
    </div>
    <div class="col">
      <label for="number" class="form-label">Number</label>
      <input
        bind:value={number}
        type="text"
        name="number"
        class="form-control col"
        id="number"
        required
      />
    </div>
  </div>
  <div class="mb-3 row">
    <div class="col">
      <label for="city" class="form-label">City</label>
      <input
        bind:value={city}
        type="text"
        name="city"
        class="form-control col"
        id="city"
        required
      />
    </div>
    <div class="col">
      <label for="province" class="form-label">Province</label>
      <input
        bind:value={province}
        type="text"
        name="province"
        class="form-control col"
        id="province"
        required
      />
    </div>
  </div>
  <div class="mb-3 row">
    <div class="col">
      <label for="cp" class="form-label">Postal code</label>
      <input
        bind:value={cp}
        type="number"
        name="cp"
        class="form-control col"
        id="cp"
        required
      />
    </div>
    <div class="col">
      <label for="country" class="form-label">Country</label>
      <input
        bind:value={country}
        type="text"
        name="country"
        class="form-control col"
        id="country"
        required
      />
    </div>
  </div>
  <div class="mb-3 row">
    <div class="col">
      <label for="price" class="form-label">€ / night</label>
      <input
        bind:value={price}
        type="number"
        name="price"
        class="form-control"
        id="price"
        required
      />
    </div>
    <div class="col">
      <label for="photos" class="form-label">Photos</label>
      <input bind:files name="photos" type="file" class="form-control" multiple />
    </div>
  </div>
  <button type="submit" class="btn btn-primary mb-3">
    {#if loading}
    <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
    <span class="sr-only">Loading...</span>
    {:else}
    <span>Publish your House</span>
    {/if}
  </button>
  <div class="progress">
    <div class="progress-bar" style="width: {publishProgress}%" role="progressbar"></div>
  </div>
  {#if publishProgress === 100}
    <span>Your house is almost published, wait a few seconds...</span>
  {/if}
</form>
