const docContent = document.getElementById('doc-content');
const navLinks = document.querySelectorAll('#navmenu a');

function setActiveLink(activeLink) {
  navLinks.forEach(link => link.classList.remove('active'));
  activeLink.classList.add('active');
}

function loadPageIntoIframe(page) {
  docContent.innerHTML = `
    <iframe 
      src="${page}" 
      style="width: 100%; height: 800px; border: none;"
      title="Documentation Content">
    </iframe>
  `;
}

navLinks.forEach(link => {
  link.addEventListener('click', event => {
    event.preventDefault();

    const page = link.dataset.page;
    if (!page) return;

    setActiveLink(link);
    loadPageIntoIframe(page);
  });
});
