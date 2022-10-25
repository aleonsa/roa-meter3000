
    $(document).ready(function () {


      const config_temp = {
          type: 'line',
          data: {
              labels: Array(30).fill("0000-00-00 00:00:00"),
              datasets: [{
                  label: "Temperature",
                  backgroundColor: 'rgb(255, 99, 132)',
                  borderColor: 'rgb(255, 99, 132)',
                  data: Array(30).fill(null),
                  fill: false,
              }],
          },
          options: {
              responsive: true,
              title: {
                  display: true,
                  text: 'Temperature'
              },
              tooltips: {
                  mode: 'index',
                  intersect: false,
              },
              hover: {
                  mode: 'nearest',
                  intersect: true
              },
              scales: {
                  xAxes: [{
                      display: true,
                      scaleLabel: {
                          display: true,
                          labelString: 'Time'
                      }
                  }],
                  yAxes: [{
                      display: true,
                      scaleLabel: {
                          display: true,
                          labelString: 'Celsius'
                      }
                  }]
              }
          }
      };
      const config_humi = {
        type: 'line',
        data: {
            labels: Array(30).fill("0000-00-00 00:00:00"),
            datasets: [{
                label: "Humidity",
                backgroundColor: 'rgb(102, 153, 255)',
                borderColor: 'rgb(102, 153, 255)',
                data: Array(30).fill(null),
                fill: false,
            }],
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Humidity'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: '%'
                    }
                }]
            }
        }
      };
      const config_pres = {
        type: 'line',
        data: {
            labels: Array(30).fill("0000-00-00 00:00:00"),
            datasets: [{
                label: "Pressure",
                backgroundColor: 'rgb(255, 198, 26)',
                borderColor: 'rgb(255, 198, 26)',
                data: Array(30).fill(null),
                fill: false,
            }],
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Pressure'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'hPa'
                    }
                }]
            }
        }
      };

      var ax = {
        label: "ax",
        data: Array(30).fill(null),
        fill: false,
        lineTension: 0,
        fill: false,
        borderColor: 'red'
      };
      var ay = {
        label: "ay",
        data: Array(30).fill(null),
        fill: false,
        lineTension: 0,
        fill: false,
        borderColor: 'blue'
      };
      var az = {
        label: "az",
        data: Array(30).fill(null),
        fill: false,
        lineTension: 0,
        fill: false,
        borderColor: 'green'
      };
      var gx = {
        label: "gx",
        data: Array(30).fill(null),
        fill: false,
        lineTension: 0,
        fill: false,
        borderColor: 'aquamarine'
      };
      var gy = {
        label: "gy",
        data: Array(30).fill(null),
        fill: false,
        lineTension: 0,
        fill: false,
        borderColor: 'salmon'
      };
      var gz = {
        label: "gz",
        data: Array(30).fill(null),
        fill: false,
        lineTension: 0,
        fill: false,
        borderColor: 'violet'
      };
      
      var acel_data = {
        labels: Array(30).fill("0000-00-00 00:00:00"),
        datasets: [ax, ay, az, gx, gy, gz]
      }
      const config_acel = {
        type: 'line',
        data: acel_data,
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Aceleration/Gyroscope'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Value'
                    }
                }]
            }
        }
      };

      const context_temp = document.getElementById('temperature').getContext('2d');
      const context_humi = document.getElementById('humidity').getContext('2d');
      const context_pres = document.getElementById('pressure').getContext('2d');
      const context_acel = document.getElementById('aceleration').getContext('2d');

      const chart_temp = new Chart(context_temp, config_temp);
      const chart_humi = new Chart(context_humi, config_humi);
      const chart_pres = new Chart(context_pres, config_pres);
      const chart_acel = new Chart(context_acel, config_acel);

      const source = new EventSource("/chart-data");

      source.onmessage = function (event) {
          const data = JSON.parse(event.data);
          if (config_temp.data.labels.length === 30) {
              config_temp.data.labels.shift();
              config_temp.data.datasets[0].data.shift();
          }
          config_temp.data.labels.push(data.time);
          config_temp.data.datasets[0].data.push(data.tvalue);
          chart_temp.update();
          if (config_humi.data.labels.length === 30) {
              config_humi.data.labels.shift();
              config_humi.data.datasets[0].data.shift();
          }
          config_humi.data.labels.push(data.time);
          config_humi.data.datasets[0].data.push(data.hvalue);
          chart_humi.update();
          if (config_pres.data.labels.length === 30) {
            config_pres.data.labels.shift();
            config_pres.data.datasets[0].data.shift();
          }
          config_pres.data.labels.push(data.time);
          config_pres.data.datasets[0].data.push(data.pvalue);
          chart_pres.update();
          if (config_acel.data.labels.length === 30) {
            config_acel.data.labels.shift();
            config_acel.data.datasets[0].data.shift();
            config_acel.data.datasets[1].data.shift();
            config_acel.data.datasets[2].data.shift();
            config_acel.data.datasets[3].data.shift();
            config_acel.data.datasets[4].data.shift();
            config_acel.data.datasets[5].data.shift();
          }
          config_acel.data.labels.push(data.time);
          config_acel.data.datasets[0].data.push(data.axvalue);
          config_acel.data.datasets[1].data.push(data.ayvalue);
          config_acel.data.datasets[2].data.push(data.azvalue);
          config_acel.data.datasets[3].data.push(data.gxvalue);
          config_acel.data.datasets[4].data.push(data.gyvalue);
          config_acel.data.datasets[5].data.push(data.gzvalue);
          chart_acel.update();
      }
  });

  $(function() {
    $('button#on').on('click', function(e) {
      e.preventDefault()
      $.getJSON('/on',
          function(data) {
        //do nothing
      });
      return false;
    });
  });
  
  $(function() {
    $('button#off').on('click', function(e) {
      e.preventDefault()
      $.getJSON('/off',
          function(data) {
        //do nothing
      });
      return false;
    });
  });