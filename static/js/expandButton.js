document.addEventListener('DOMContentLoaded', function () {
   let fullscreenActivated = false 
   const expandButton = document.getElementById('expandButton');
   const fullscreenComponent = document.querySelector('.editor-component');

   expandButton.addEventListener('click', function () {
      fullscreenComponent.classList.toggle('fullscreen');
      fullscreenActivated = !fullscreenActivated
      
      if(fullscreenActivated){
         expandButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" fill="none" viewBox="0 0 48 48"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="4" d="M33 6v9h9M15 6v9H6M15 42v-9H6M33 42v-9h8.9"></path></svg>'
      }else{
         expandButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" fill="none" viewBox="0 0 48 48"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="4" d="M33 6h9v9M42 33v9h-9M15 42H6v-9M6 15V6h9"></path></svg>'
      }
   });

});