const checkbox = document.getElementById('show-password');
const passwordInput = document.getElementById('password');

// Adicionar um ouvinte de eventos para detectar alterações no estado do checkbox
checkbox.addEventListener('change', function () {
   // Verificar se o checkbox está marcado
   passwordInput.type = checkbox.checked ? 'text' : 'password';
});