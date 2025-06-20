document.addEventListener("DOMContentLoaded", () => {
    const countrySelect = document.getElementById('id_default_country');
    if (countrySelect) {
      const setColor = () => {
        countrySelect.style.color = countrySelect.value ? '#000' : '#6c757d';
      };
      setColor();
      countrySelect.addEventListener('change', setColor);
    }
  });
  