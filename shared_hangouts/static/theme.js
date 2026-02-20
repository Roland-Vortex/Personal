function setTheme(theme) {
    document.body.className = theme;
    localStorage.setItem("theme", theme);
}

window.onload = function() {
    const saved = localStorage.getItem("theme");
    if (saved) {
        document.body.className = saved;
    }
}