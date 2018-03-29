export default {

    weather:{
        status:false,
        chart: {
            zoomType: 'xy'
        },
        title: {
            text: 'Weather Data for US States'
        },
        subtitle: {
            text: ''
        },
        xAxis: [{
            categories:[],
            crosshair: true
        }],
        yAxis: [{ // Primary yAxis
            labels: {
                format: '{value}°C'
            },
            title: {
                text: 'Temperature'
            },
            opposite: true

        }, { // Secondary yAxis
            gridLineWidth: 0,
            title: {
                text: 'Humidity',
            },
            labels: {
                format: '{value} '
            }

        }, { // Tertiary yAxis
            gridLineWidth: 0,
            title: {
                text: 'Pressure'
            },
            labels: {
                format: '{value} mb'
            },
            opposite: true
        }],
        tooltip: {
            shared: true
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            x: 80,
            verticalAlign: 'top',
            y: 55,
            floating: true
        },
        series: [{
            name: 'humidity',
            type: 'column',
            yAxis: 1,
            data:[],
            tooltip: {
                valueSuffix: ' '
            }

        },
         {
         name: 'pressure',
         type: 'spline',
         yAxis: 2,
         data: [],
         marker: {
             enabled: false
         },
         dashStyle: 'shortdot',
         tooltip: {
             valueSuffix: ' mb'
         }

     }, {
         name: 'temp',
         type: 'spline',
         data: [],
         tooltip: {
             valueSuffix: ' °C'
         }
     }]
    }
}