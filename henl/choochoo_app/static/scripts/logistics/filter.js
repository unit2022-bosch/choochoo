const orders = document.getElementsByClassName("orders")[0];
for (const [column_index, column_name] of window.filterFields) {
  const input = document.getElementById(`${column_name}-filter`);
  console.log(window.multipleWarehouses);
  input.addEventListener("input", () => {
    const substring = input.value;
    for (const row of orders.getElementsByTagName("tr")) {
      if (row.children[0].tagName === "TD") {
        row.hidden = !row.children[column_index].innerText.includes(substring);
      }
    }
  });
}
