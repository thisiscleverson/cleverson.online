document.getElementById('markdown-content').addEventListener('input', function () {
   // Get references to the elements
   const markdownContent = document.getElementById('markdown-content');
   const htmlPreview = document.getElementById('html-preview');

   // Convert Markdown to HTML
   htmlPreview.innerHTML = marked.parse(markdownContent.value);
    
});