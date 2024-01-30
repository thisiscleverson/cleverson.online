

const BASEURL = window.location.origin

const draftButton =  () => {

   const title = document.getElementById("title")
   const body  = document.getElementById("markdown-content")
   const description =  document.getElementById("description")

   const dataJson = {
      "title": title.value,
      "body": body.value,
      "description": description.value
   }

   fetch(BASEURL + '/draft', {
      method: "POST",
      headers: {
         'Accept': 'application/json',
         'Content-Type': 'application/json'
      },
      body: JSON.stringify(dataJson)
   }).then((response) => { 
      if(response.status == 200){
         window.location = "/admin"
      }else{
         throw `error with status ${response.status}`;
      }
   }).catch((error) => {
      console.error(error)
      console.log('Ops, ocorreu um erro inesperado ao fazer a requisição com API!')
   })
}; 


const updateButton = (draft_id) => {
   const title = document.getElementById("title")
   const body  = document.getElementById("markdown-content")
   const description =  document.getElementById("description")

   const dataJson = {
      "title": title.value,
      "body": body.value,
      "description": description.value
   }

   fetch(BASEURL + `/update/${draft_id}`, {
      method: "POST",
      headers: {
         'Accept': 'application/json',
         'Content-Type': 'application/json'
      },
      body: JSON.stringify(dataJson)
   }).then((response) => { 
      if(response.status == 200){
         window.location = "/admin"
      }else{
         throw `error with status ${response.status}`;
      }
   }).catch((error) => {
      console.error(error)
      console.log('Ops, ocorreu um erro inesperado ao fazer a requisição com API!')
   })
}

const publish = (draft_id) => {
   const title = document.getElementById("title")
   const body  = document.getElementById("markdown-content")
   const description =  document.getElementById("description")

   const dataJson = {
      "title": title.value,
      "body": body.value,
      "description": description.value
   }

   fetch(BASEURL + `/update/${draft_id}`, {
      method: "PUT",
      headers: {
         'Accept': 'application/json',
         'Content-Type': 'application/json'
      },
      body: JSON.stringify(dataJson)
   }).then((response) => { 
      if(response.status == 200){
         window.location = "/admin"
      }else{
         throw `error with status ${response.status}`;
      }
   }).catch((error) => {
      console.error(error)
      console.log('Ops, ocorreu um erro inesperado ao fazer a requisição com API!')
   })
}