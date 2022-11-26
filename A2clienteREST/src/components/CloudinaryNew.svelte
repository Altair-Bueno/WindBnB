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
    let image : string[] = [];
    if(files){
      //image = await upload(cloudName, uploadPreset, files[0]).then(x => x.json()).then(x => [x.url]);
      //image = await Promise.all(files.map((fich : any) => upload(cloudName, uploadPreset, fich).then(x => x.json()).then(x => x.url)));
      for (let i = 0; i < files.length; i++){
          let fich = files[i];
          let res = await upload(cloudName, uploadPreset, fich).then(x => x.json()).then(x => x.url)
          image.push(res);
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
        image
      }),
    }).then(x => x.json());
    window.location.href = res.redirect;   
  }
</script>

<!--<form action="/houses/new/newHandler" method="post">-->
  <form on:submit|preventDefault={handleOnSubmit}>
  <!-- <input hidden value="EXAMPLE_USER_HARDCODED" name="userId" /> TODO -->
  <div class="mb-3">
    <label for="title" class="form-label">Título</label>
    <input bind:value={title} type="text" name="title" class="form-control" id="title" aria-describedby="titleHelp" required>

  </div>
  <div class="mb-3">
    <label for="description" class="form-label">Descripción</label>
    <input bind:value={description} type="text" name="description" class="form-control" id="description">
  </div>
  <div class="mb-3">
    <label for="street" class="form-label">Calle</label>
    <input bind:value={street} type="text" name="street" class="form-control" id="street" required>
    <label for="number" class="form-label">Número</label>
    <input bind:value={number} type="text" name="number" class="form-control" id="number" required>
    <label for="city" class="form-label">Ciudad</label>
    <input bind:value={city} type="text" name="city" class="form-control" id="city" required>
    <label for="province" class="form-label">Provincia</label>
    <input bind:value={province} type="text" name="province" class="form-control" id="province" required>
    <label for="cp" class="form-label">Código postal</label>
    <input bind:value={cp} type="text" name="cp" class="form-control" id="cp" required>
    <label for="country" class="form-label">País</label>
    <input bind:value={country} type="text" name="country" class="form-control" id="country" required>
  </div>
  <div class="mb-3">
    <label for="price" class="form-label">Precio por noche</label>
    <input bind:value={price} type="number" name="price" class="form-control" id="price" required>
</div>
  <input bind:files type="file" multiple/>
  <button type="submit" class="btn btn-primary">Crear</button>
</form>
