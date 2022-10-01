window.onload = () => {

    [...document.querySelector(`#Mobility`).options]
      .filter(x => x.value === "14")[0]
      .setAttribute('selected', true);
  };