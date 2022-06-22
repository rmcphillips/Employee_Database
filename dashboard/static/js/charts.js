const endPoint = "chart/"
var defaultData = []
var labels = []

$.ajax({
    method: "GET",
    url: endPoint,
    success: function (data) {
        labels = data.labels
        defaultData = data.default
        var ctx = document.getElementById('myChart');
        var myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: defaultData,
                    backgroundColor: [
                        'rgb(67, 170, 139)',
                        'rgb(77, 144, 142)',
                        'rgb(87, 117, 144)',
                        'rgb(39, 125, 161)',
                        'rgb(144, 190, 109)',
                        'rgb(249, 65, 68)',
                        'rgb(249, 199, 79)',
                        'rgb(249, 132, 74)',
                        'rgb(248, 150, 30)',
                        'rgb(150, 50, 30)',
                    ]
                }]
            },
        });
    },
    error: function (error) {
        console.log(error)
    },
})