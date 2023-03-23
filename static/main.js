async function loadTickers() {
  const response = await fetch("/static/stocks.json");

  const stocks = await response.json();

  const select = document.getElementById("ticker");

  for (const stock of stocks) {
    const option = document.createElement("option");
    option.value = stock;
    option.innerText = stock;

    select.appendChild(option);
  }
}

loadTickers();
