document.addEventListener("DOMContentLoaded", function() {
    // Afficher la modal de bienvenue au chargement de la page
    let modal = document.getElementById('welcomeModal');
    modal.style.display = 'block';

    // Fermer la modal en cliquant sur le bouton de fermeture
    let closeBtn = document.getElementsByClassName('close')[0];
    closeBtn.onclick = function() {
        modal.style.display = 'none';
    }

    // Fermer la modal si l'utilisateur clique en dehors de celle-ci
    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    }
});

// Vidéo flottante:

document.addEventListener('DOMContentLoaded', () => {
    const floatingVideoContainer = document.getElementById('floating-video-container');
    const floatingVideo = document.getElementById('floating-video');
    const playlist = document.getElementById('playlist');
    const playlistVideos = playlist.querySelectorAll('video');
    const closeButton = document.getElementById('close-button');
    const toggleSizeButton = document.getElementById('toggle-size-button');
  
    floatingVideoContainer.addEventListener('mouseover', () => {
      floatingVideo.play();
    });
  
    floatingVideoContainer.addEventListener('mouseleave', () => {
      floatingVideo.pause();
    });
  
    toggleSizeButton.addEventListener('click', () => {
      if (floatingVideoContainer.style.width === '600px') {
        floatingVideoContainer.style.width = '300px';
        floatingVideoContainer.style.height = 'auto';
        playlist.style.display = 'none';
      } else {
        floatingVideoContainer.style.width = '600px';
        floatingVideoContainer.style.height = 'auto';
        playlist.style.display = 'block';
      }
    });
  
    closeButton.addEventListener('click', () => {
      floatingVideoContainer.style.display = 'none';
    });
  
    playlistVideos.forEach(video => {
      video.addEventListener('click', () => {
        floatingVideo.src = video.src;
        floatingVideo.play();
      });
    });
  });


  $(document).ready(function(){
    $('.carousel').carousel({
      padding: 200
  });
  autoplay();
  function autoplay() {
    $('.carousel').carousel('next');
    setTimeout(autoplay, 4500);
  }
  });