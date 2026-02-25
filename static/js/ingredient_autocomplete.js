/**
 * Ingredient Autocomplete
 *
 * Logic:
 * 1. Find all inputs with [data-autocomplete-url]
 * 2. On input, fetch suggestions from the URL
 * 3. Show suggestions in a dropdown below the input
 */

document.addEventListener('DOMContentLoaded', () => {
  const initAutocomplete = (input) => {
    if (input.dataset.autocompleteInitialized) {
      return;
    }
    input.dataset.autocompleteInitialized = 'true';

    const url = input.dataset.autocompleteUrl;
    let timeout = null;
    let dropdown = null;

    const removeDropdown = () => {
      if (dropdown) {
        dropdown.remove();
        dropdown = null;
      }
    };

    const showSuggestions = (suggestions) => {
      removeDropdown();
      if (suggestions.length === 0) {
        return;
      }

      dropdown = document.createElement('ul');
      dropdown.className = 'autocomplete-dropdown';
      // Basic styling - in a real app this would be in CSS
      Object.assign(dropdown.style, {
        position: 'absolute',
        zIndex: '1000',
        background: 'var(--color-surface, white)',
        border: '1px solid var(--color-border, #ccc)',
        borderRadius: 'var(--radius, 4px)',
        listStyle: 'none',
        padding: '0',
        margin: '0',
        width: `${input.offsetWidth}px`,
        maxHeight: '200px',
        overflowY: 'auto',
        boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
      });

      suggestions.forEach((text) => {
        const li = document.createElement('li');
        li.textContent = text;
        Object.assign(li.style, {
          padding: '8px 12px',
          cursor: 'pointer',
          borderBottom: '1px solid var(--color-border-subtle, #eee)',
        });

        li.addEventListener('mouseenter', () => {
          li.style.background = 'var(--color-surface-hover, #f5f5f5)';
        });
        li.addEventListener('mouseleave', () => {
          li.style.background = 'none';
        });

        li.addEventListener('click', () => {
          input.value = text;
          removeDropdown();
        });
        dropdown.appendChild(li);
      });

      // Position dropdown
      const rect = input.getBoundingClientRect();
      dropdown.style.top = `${window.scrollY + rect.bottom}px`;
      dropdown.style.left = `${window.scrollX + rect.left}px`;

      document.body.appendChild(dropdown);
    };

    input.addEventListener('input', () => {
      clearTimeout(timeout);
      const query = input.value.trim();
      if (query.length < 2) {
        removeDropdown();
        return;
      }

      timeout = setTimeout(async () => {
        try {
          const response = await fetch(
              `${url}?q=${encodeURIComponent(query)}`,
          );
          const data = await response.json();
          showSuggestions(data.suggestions);
        } catch (err) {
          console.error('Autocomplete fetch failed', err);
        }
      }, 300);
    });

    // Hide dropdown on blur (with delay to allow clicks)
    input.addEventListener('blur', () => {
      setTimeout(removeDropdown, 200);
    });

    // Reposition on window resize
    window.addEventListener('resize', removeDropdown);
  };

  // Initialize existing inputs
  document.querySelectorAll('[data-autocomplete-url]').
      forEach(initAutocomplete);

  // Watch for new inputs (formset additions)
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (node.nodeType === 1) { // Element
          if (node.hasAttribute('data-autocomplete-url')) {
            initAutocomplete(node);
          }
          node.querySelectorAll('[data-autocomplete-url]').
              forEach(initAutocomplete);
        }
      });
    });
  });

  const container = document.getElementById('ingredient-formset');
  if (container) {
    observer.observe(container, {childList: true, subtree: true});
  }
});
