// Load last theme
const themeSelect = document.getElementById('theme-select');
const lastTheme = localStorage.getItem('theme') || 'red-white';
document.body.className = lastTheme;
themeSelect.value = lastTheme;

// Change theme
themeSelect.addEventListener('change', () => {
    document.body.className = themeSelect.value;
    localStorage.setItem('theme', themeSelect.value);
});
