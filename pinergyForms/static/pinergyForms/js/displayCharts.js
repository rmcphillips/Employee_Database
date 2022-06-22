
const navbar = document.getElementById("navbar")
navbar.hidden = "true"

const endPoint = "/pinergyForms/chart/"
var salesB2B = []
var salesB2C = []
var retention = []

$.ajax({
    method: "GET",
    url: endPoint,
    success: function (data) {
        var ctx = document.getElementById('chartSalesB2B');
        var chartSalesB2B = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Current', 'Target'],
                datasets: [{
                    data: data.salesB2B,
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
        var ctx = document.getElementById('chartSalesB2C');
        var chartSalesB2C = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Current', 'Target'],
                datasets: [{
                    data: data.salesB2C,
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

