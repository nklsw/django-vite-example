import 'unpoly/unpoly.js';
import 'unpoly/unpoly.css';

up.log.enable()
up.fragment.config.navigateOptions.cache = false

up.compiler('form', function() {
    // Define the btn-spinner preview
    up.preview('btn-spinner', function(preview) {
      // Find the submit button
      let button = findButton(preview.origin);
      
      // Preserve button dimensions to prevent layout shifts
      preview.setStyle(button, { 
        height: button.offsetHeight + 'px', 
        width: button.offsetWidth + 'px'
      });
      
      // Replace button content with spinner
      preview.swapContent(button, '<span class="btn-spinner"></span>');
    });
    
    function findButton(origin) {
      if (origin.matches('.btn, button[type="submit"]')) {
        return origin;
      } else {
        let form = origin.closest('form');
        return form.querySelector('button[type="submit"]');
      }
    }
  });