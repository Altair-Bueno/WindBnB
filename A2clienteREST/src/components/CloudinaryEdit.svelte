<script lang="ts">
    import { EditVivienda, ViviendaApi } from "../api/A2viviendasREST";
    import type {Vivienda} from "../api/A2viviendasREST";
    import AppConfig from "../config";
    export let cloudName = "";
    export let uploadPreset = "";
    export let vivienda : Vivienda;
    
    let files: any;

    const loc = vivienda.location;
    const loc_splitted = loc.split(", ");

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
        for (let i = 0; i < files.length; i++){
            let fich = files[i];
            let res = await upload(cloudName, uploadPreset, fich).then(x => x.json()).then(x => x.url)
            image.push(res);
        }
      } else {
        image = vivienda.urlPhoto ?? [];
      }
      const res = await fetch("/houses/edit/editHandler", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
            idCasa: vivienda.id,
            title: vivienda.title,
            description: vivienda.description,
            street: loc_splitted[0],
            number: loc_splitted[1],
            city: loc_splitted[2],
            province: loc_splitted[3],
            cp: loc_splitted[4],
            country: loc_splitted[5],
            price: vivienda.price,
            image
        }),
      }).then(x => x.json());
      window.location.href = res.redirect;   
    }
  </script>
  
    <form on:submit|preventDefault={handleOnSubmit}>
    <input type="text" value={vivienda.id} name="idCasa" hidden>
        <div class="mb-3">
          <label for="title" class="form-label">Title</label>
          <input bind:value={vivienda.title} type="text" name="title" class="form-control" id="title" aria-describedby="title" required>
        </div>
        <div class="mb-3">
          <label for="description" class="form-label">Description</label>
          <input type="text" bind:value={vivienda.description} name="description" class="form-control" id="description">
        </div>
        <div class="mb-3">
          <label for="street" class="form-label">Street</label>
          <input type="text" bind:value={loc_splitted[0]} name="street" class="form-control" id="street" required>
          <label for="number" class="form-label">Number</label>
          <input type="text" bind:value={loc_splitted[1]} name="number" class="form-control" id="number" required>
          <label for="number" class="form-label">City</label>
          <input type="text" bind:value={loc_splitted[2]} name="city" class="form-control" id="city"  required>
          <label for="province" class="form-label">Province</label>
          <input type="text" bind:value={loc_splitted[3]} name="province" class="form-control" id="province"  required>
          <label for="cp" class="form-label">Postal code</label>
          <input type="text" bind:value={loc_splitted[4]} name="cp" class="form-control" id="cp"  required>
          <label for="country" class="form-label">Country</label>
          <input type="text" bind:value={loc_splitted[5]} name="country" class="form-control" id="country" required>
        </div>
        <div class="mb-3">
          <label for="price" class="form-label">Price per night</label>
          <input type="number" bind:value={vivienda.price} name="price" class="form-control" id="price" required>
      </div>
        
    <input bind:files type="file" multiple/>
    <button type="submit" class="btn btn-primary">Edit data</button>
  </form>
  