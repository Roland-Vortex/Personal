const select = document.getElementById("themeSelect");
select.value = document.body.className;

select.addEventListener("change", async () => {
  const theme = select.value;
  document.body.className = theme;
  await fetch("/change_theme", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `theme=${theme}`
  });
});
