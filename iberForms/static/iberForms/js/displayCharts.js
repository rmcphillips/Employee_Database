
const navbar = document.getElementById("navbar")
navbar.hidden = "true"

const endPoint = "/iberForms/chart/"
var sales = []
var care = []
var retention = []

$.ajax({
    method: "GET",
    url: endPoint,
    success: function (data) {
        var ctx = document.getElementById('chartSales');
        var chartSales = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Current', 'Target'],
                datasets: [{
                    data: data.sales,
                    backgroundColor: [
                        'rgb(67, 170, 139)',
                        'rgb(39, 125, 161)',
                    ]
                }]
            },
            options: {
                legend: {
                    display: false
                },
                tooltips: {
                    callbacks: {
                        label: function (tooltipItem) {
                            return tooltipItem.yLabel;
                        }
                    }
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    },
})


$.ajax({
    method: "GET",
    url: endPoint,
    success: function (data) {
        var ctx = document.getElementById('chartRetention');
        var chartRetention = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Current', 'Target'],
                datasets: [{
                    data: data.retention,
                    backgroundColor: [
                        'rgb(67, 170, 139)',
                        'rgb(39, 125, 161)',
                    ]
                }]
            },
            options: {
                legend: {
                    display: false
                },
                tooltips: {
                    callbacks: {
                        label: function (tooltipItem) {
                            return tooltipItem.yLabel;
                        }
                    }
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    },
})

window.setTimeout(function () {
    window.location.reload();
}, 300000);

