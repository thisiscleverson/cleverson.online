const BASEURL = window.location.origin

const buttonDeletePost = (id) => {
   
   fetch(BASEURL + `/api/delete/post/${id}`, {
      method: "DELETE",
      headers: {
         'Accept': 'application/json',
         'Content-Type': 'application/json'
      }
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