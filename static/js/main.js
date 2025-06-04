document.addEventListener("DOMContentLoaded", function () {
    const target = document.getElementById("vanta-bg");
    if (target) {
      VANTA.BIRDS({
        el: "#vanta-bg",
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 200.00,
        minWidth: 200.00,
        scale: 1.00,
        scaleMobile: 1.00,
        backgroundColor: 0xa96ccc,
        birdSize: 1.30
      });
    } else {
      console.warn("[VANTA] #vanta-bg not found.");
    }
  });
  