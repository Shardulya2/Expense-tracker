document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById('expenseChart').getContext('2d');

  const labels = JSON.parse(document.getElementById('chart-labels').textContent);
  const data = JSON.parse(document.getElementById('chart-data').textContent);

  const chart = new Chart(ctx, {
    type: 'bar', // You can also use 'pie', 'line', etc.
    data: {
      labels: labels,
      datasets: [{
        label: 'Expenses by Category',
        data: data,
        backgroundColor: [
          '#007bff',
          '#dc3545',
          '#ffc107',
          '#28a745',
          '#6610f2',
          '#6f42c1'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0
          }
        }
      }
    }
  });
});
