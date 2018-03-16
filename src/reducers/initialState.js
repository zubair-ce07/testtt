export default {

    config:{
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
                format: '{value}°C',
                style: {
                    //color: Highcharts.getOptions().colors[2]
                }
            },
            title: {
                text: 'Temperature',
                style: {
                    //color: Highcharts.getOptions().colors[2]
                }
            },
            opposite: true

        }, { // Secondary yAxis
            gridLineWidth: 0,
            title: {
                text: 'Humidity',
                style: {
                    // color: Highcharts.getOptions().colors[0]
                }
            },
            labels: {
                format: '{value} ',
                style: {
                    // color: Highcharts.getOptions().colors[0]
                }
            }

        }, { // Tertiary yAxis
            gridLineWidth: 0,
            title: {
                text: 'Pressure',
                style: {
                    //color: Highcharts.getOptions().colors[1]
                }
            },
            labels: {
                format: '{value} mb',
                style: {
                    //color: Highcharts.getOptions().colors[1]
                }
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
            floating: true,
            //backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
        },
        series: [{
            name: 'humidity',
            type: 'column',
            yAxis: 1,
            data:[],
            tooltip: {
                valueSuffix: ' mm'
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