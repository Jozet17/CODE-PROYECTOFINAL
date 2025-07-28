document.addEventListener('DOMContentLoaded', () => {
  const menu = document.getElementById('menu');
  const abrirMenu = document.getElementById('abrir-menu');
  const botonesAuth = document.getElementById('botones-auth');
  const cerrarSesion = document.getElementById('cerrar-sesion');

  if (abrirMenu && menu) {
    abrirMenu.addEventListener('click', (e) => {
      e.stopPropagation();
      menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
    });

    document.addEventListener('click', (e) => {
      if (!menu.contains(e.target) && !abrirMenu.contains(e.target)) {
        menu.style.display = 'none';
      }
    });
  }

  // Estas variables deben ser definidas desde el HTML con Flask
  if (typeof usuarioIniciado !== 'undefined' && usuarioIniciado) {
    if (botonesAuth) {
      const registroBtn = botonesAuth.querySelector('.boton-registro');
      const sesionBtn = botonesAuth.querySelector('.boton-sesion');
      if (registroBtn) registroBtn.style.display = 'none';
      if (sesionBtn) sesionBtn.style.display = 'none';
    }
    if (cerrarSesion) cerrarSesion.style.display = 'block';
  } else {
    if (cerrarSesion) cerrarSesion.style.display = 'none';
  }

  if (typeof mensaje !== 'undefined' && mensaje) {
    const div = document.createElement('div');
    div.textContent = mensaje;
    div.style.position = 'fixed';
    div.style.top = '50%';
    div.style.left = '50%';
    div.style.transform = 'translate(-50%, -50%)';
    div.style.background = '#1eff9a';
    div.style.color = '#000';
    div.style.padding = '15px 25px';
    div.style.fontSize = '20px';
    div.style.borderRadius = '12px';
    div.style.zIndex = '9999';
    div.style.boxShadow = '0 0 10px rgba(0,0,0,0.5)';
    document.body.appendChild(div);

    setTimeout(() => {
      div.remove();
    }, 3000);
  }
});
