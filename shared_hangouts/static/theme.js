function setTheme(theme) {
    localStorage.setItem("theme", theme);
    applyTheme(theme);
}

function applyTheme(theme) {
    const body = document.body;

    const themes = {
        pink: ["pink","black"],
        red: ["red","white"],
        lightblue: ["lightblue","black"],
        darkblue: ["darkblue","white"],
        green: ["green","white"],
        purple: ["purple","white"],
        yellow: ["yellow","black"]
    };

    body.style.backgroundColor = themes[theme][0];
    body.style.color = themes[theme][1];
}

window.onload = () => {
    const saved = localStorage.getItem("theme") || "pink";
    applyTheme(saved);
};