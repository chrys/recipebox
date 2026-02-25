/**
 * Recipe List View Toggle
 * 
 * Logic:
 * 1. Listen for click on #view-toggle
 * 2. Toggle 'view-mode-list' class on body or container
 * 3. Persist choice to localStorage
 * 4. Restore choice on page load
 */

document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('view-toggle');
    const container = document.getElementById('recipe-view-container');
    const storageKey = 'recipe_list_view_mode';

    if (!toggleBtn || !container) return;

    const setViewMode = (mode) => {
        if (mode === 'list') {
            container.classList.add('view-mode-list');
            toggleBtn.textContent = '☰'; // Icon for list
            toggleBtn.title = 'Switch to Grid View';
        } else {
            container.classList.remove('view-mode-list');
            toggleBtn.textContent = '⊞'; // Icon for grid
            toggleBtn.title = 'Switch to List View';
        }
        localStorage.setItem(storageKey, mode);
    };

    // Initialize from localStorage
    const savedMode = localStorage.getItem(storageKey);
    if (savedMode) {
        setViewMode(savedMode);
    }

    toggleBtn.addEventListener('click', () => {
        const currentMode = container.classList.contains('view-mode-list') ? 'list' : 'grid';
        setViewMode(currentMode === 'list' ? 'grid' : 'list');
    });
});
