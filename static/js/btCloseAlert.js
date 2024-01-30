const alertButton = document.querySelector('.bt-close') 

alertButton.addEventListener('click', function(){
   const alert = document.querySelector('.alert')

   // Certifique-se de que o elemento pai existe antes de removê-lo
   if (alert) {
      alert.remove();
   }
})