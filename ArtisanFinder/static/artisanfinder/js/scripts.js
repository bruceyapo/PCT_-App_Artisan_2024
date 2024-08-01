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
    $('.slideshow').slideshow({
      padding: 200
  });
  autoplay();
  function autoplay() {
    $('.slideshow').slideshow('next');
    setTimeout(autoplay, 5500);
  }
  });

  // Filtre selon la localisation :

  function filterByLocation() {
    const locationInput = document.getElementById('location-input').value.toLowerCase();
    const cards = document.querySelectorAll('.carpenter-card');
    let found = false;

    cards.forEach(card => {
        const cardLocation = card.getAttribute('data-location').toLowerCase();
        if (cardLocation.includes(locationInput)) {
            card.style.display = 'block';
            found = true;
        } else {
            card.style.display = 'none';
        }
    });

    const noResultsMessage = document.getElementById('no-results');
    if (found) {
        noResultsMessage.style.display = 'none';
    } else {
        noResultsMessage.style.display = 'block';
    }
}

// Affiche la selection :

function updateSelectedOption() {
  var select = document.getElementById("options");
  var selectedOption = select.options[select.selectedIndex].text;
  document.getElementById("selectedOption").innerText = selectedOption;
}

function displaySelectedWork() {
  const selectElement = document.getElementById('carpentry-work');
  const selectedWork = selectElement.options[selectElement.selectedIndex].text;
  const selectedWorkDiv = document.getElementById('selected-work');
  selectedWorkDiv.textContent = `Travail sélectionné : ${selectedWork}`;
}

// Affichage dynamique des publicités
function loadAdvertisements() {
  fetch('/static/json/ads.json')
      .then(response => response.json())
      .then(data => {
          const adContainer = document.querySelector('.ad-carousel');
          data.forEach(ad => {
              const adElement = document.createElement('div');
              adElement.classList.add('ad-item');
              adElement.innerHTML = `
                  <a href="${ad.link}" target="_blank">
                      <img src="${ad.image}" alt="${ad.alt}">
                  </a>
              `;
              adContainer.appendChild(adElement);
          });
      })
      .catch(error => console.error('Error loading ads:', error));
}

document.addEventListener('DOMContentLoaded', loadAdvertisements);


   //Pour l'ajout de photo au portfolio
  
    function deleteImage(imageSrc) {
      const portfolioItems = document.querySelectorAll('.portfolio-item');
      portfolioItems.forEach(item => {
        const img = item.querySelector('img');
        if (img.getAttribute('src') === imageSrc) {
          item.remove();
        }
      });
    }

    function submitPhotoForm() {
      document.getElementById('add-photo-form').submit();
    }


 
  //Pour afficher et masquer la carte de contact 
  
    function showContactCard() {
      document.getElementById('contact-card').style.display = 'block';
    }

    function hideContactCard() {
      document.getElementById('contact-card').style.display = 'none';
    }

// Pour l'affichage de la barre de progression sur les formulaire

    let currentStep = 0;

    function updateProgressBar() {
        const progressBar = document.getElementById('progressBar');
        const totalSteps = document.querySelectorAll('.form-step').length;
        const percentage = ((currentStep + 1) / totalSteps) * 100;
        progressBar.style.width = percentage + '%';
    }

    function showStep(step) {
        const steps = document.querySelectorAll('.form-step');
        steps.forEach((element, index) => {
            element.classList.toggle('active', index === step);
        });
        updateProgressBar();
    }

    function nextStep() {
        const steps = document.querySelectorAll('.form-step');
        const currentInputs = steps[currentStep].querySelectorAll('input, select');
        let allValid = true;

        currentInputs.forEach(input => {
            if (!input.checkValidity()) {
                input.reportValidity();
                allValid = false;
            }
        });

        if (allValid && currentStep < steps.length - 1) {
            currentStep++;
            showStep(currentStep);
        }
    }

    document.getElementById('multiStepForm').addEventListener('submit', function (event) {
        event.preventDefault();
        alert('Form submitted successfully!');
    });

    showStep(currentStep);