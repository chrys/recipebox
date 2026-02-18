/**
 * RecipeBox — Client-side JavaScript
 * Handles: ingredient formset, dark mode toggle, Django messages → oat toasts
 */

document.addEventListener('DOMContentLoaded', () => {
    // ---- Dark Mode Toggle ----
    const toggle = document.getElementById('dark-mode-toggle');
    if (toggle) {
        const saved = localStorage.getItem('theme');
        if (saved === 'dark') {
            document.body.setAttribute('data-theme', 'dark');
            toggle.textContent = '☀️';
        }
        toggle.addEventListener('click', () => {
            const isDark = document.body.getAttribute('data-theme') === 'dark';
            if (isDark) {
                document.body.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
                toggle.textContent = '🌙';
            } else {
                document.body.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                toggle.textContent = '☀️';
            }
        });
    }

    // ---- Django Messages → oat toasts ----
    const messagesEl = document.getElementById('django-messages');
    if (messagesEl && typeof ot !== 'undefined') {
        const messages = messagesEl.querySelectorAll('[data-msg]');
        messages.forEach(msg => {
            const text = msg.textContent.trim();
            const level = msg.getAttribute('data-level');
            let variant = '';
            if (level === 'success') variant = 'success';
            else if (level === 'error') variant = 'danger';
            else if (level === 'warning') variant = 'warning';
            ot.toast(text, '', { variant });
        });
    }

    // ---- Ingredient Formset Management ----
    const addBtn = document.getElementById('add-ingredient');
    const container = document.getElementById('ingredient-formset');
    const totalInput = document.getElementById('id_ingredients-TOTAL_FORMS');

    if (addBtn && container && totalInput) {
        addBtn.addEventListener('click', () => {
            const formCount = parseInt(totalInput.value);
            const emptyForm = document.getElementById('empty-ingredient-form');
            if (!emptyForm) return;

            const newForm = emptyForm.innerHTML.replace(/__prefix__/g, formCount);
            const div = document.createElement('div');
            div.className = 'ingredient-row';
            div.innerHTML = newForm;
            container.appendChild(div);
            totalInput.value = formCount + 1;
        });

        // Remove ingredient row
        container.addEventListener('click', (e) => {
            if (e.target.classList.contains('remove-ingredient')) {
                const row = e.target.closest('.ingredient-row');
                const deleteInput = row.querySelector('input[name$="-DELETE"]');
                if (deleteInput) {
                    deleteInput.value = 'on';
                    row.style.display = 'none';
                } else {
                    row.remove();
                }
            }
        });
    }

    // ---- Calendar: set date in add-recipe dialog ----
    document.querySelectorAll('.calendar-add-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const date = btn.getAttribute('data-date');
            const dateInput = document.getElementById('calendar-date-input');
            if (dateInput) {
                dateInput.value = date;
            }
        });
    });

    // ---- CSRF Helper ----
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // ---- Star Rating Interaction ----
    const ratingContainers = document.querySelectorAll('.recipe-rating');
    ratingContainers.forEach(container => {
        const recipeId = container.getAttribute('data-recipe-id');
        const stars = container.querySelectorAll('.star');

        stars.forEach(star => {
            star.addEventListener('click', () => {
                const rating = star.getAttribute('data-value');
                fetch(`/recipes/${recipeId}/rate/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({ rating: rating })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'ok') {
                        // Update stars UI
                        const currentRating = data.rating;
                        stars.forEach(s => {
                            const val = parseInt(s.getAttribute('data-value'));
                            s.textContent = val <= currentRating ? '★' : '☆';
                        });
                        if (typeof ot !== 'undefined') {
                            ot.toast('Rating updated!', '', { variant: 'success' });
                        }
                    } else {
                        if (typeof ot !== 'undefined' && data.error) {
                            ot.toast(data.error, '', { variant: 'danger' });
                        }
                    }
                })
                .catch(err => {
                    console.error('Error updating rating:', err);
                });
            });
        });
    });
});
