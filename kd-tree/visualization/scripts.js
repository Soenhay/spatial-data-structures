
function createChart(element, jsonString) {
    const ctx = document.getElementById(element);

    var jsonObjArray = JSON.parse(jsonString);
    var pointData = [];
    jsonObjArray.forEach(element => {
        pointData.push({ x: parseInt(element.X), y: parseInt(element.Y) });
    });

    const data = {
        datasets: [{
            label: 'Scatter Dataset',
            data: pointData,
            backgroundColor: 'rgb(255, 99, 132)'
        }],
    };

    const config = {
        type: 'scatter',
        data: data,
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom'
                }
            }
        }
    };

    new Chart(ctx, config);
}