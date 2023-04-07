// set up chart
var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [{
      label: 'Systolic',
      borderColor: 'rgb(255, 99, 132)',
      data: [],
      fill: false
    }, {
      label: 'Diastolic',
      borderColor: 'rgb(54, 162, 235)',
      data: [],
      fill: false
    }]
  },
  options: {
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
                labelString: 'mmHg'
              }
            }]
          }
        }
      });

      // update chart
      function updateChart(time, systolic, diastolic) {
        chart.data.labels.push(time);
        chart.data.datasets[0].data.push(systolic);
        chart.data.datasets[1].data.push(diastolic);
        chart.update();
      }

      // update latest reading
      function updateReading(bp, pulse, spo2) {
        document.getElementById('bp').innerHTML = bp;
        document.getElementById('pulse').innerHTML = pulse;
        document.getElementById('spo2').innerHTML = spo2;
      }

      // simulate readings (replace with actual data)
      setInterval(function() {
        var time = new Date().toLocaleTimeString();
        var systolic = Math.floor(Math.random() * 30) + 100;
        var diastolic = Math.floor(Math.random() * 20) + 60;
        var pulse = Math.floor(Math.random() * 20) + 60;
        var spo2 = Math.floor(Math.random() * 3) + 96;
        var bp = systolic + '/' + diastolic + 'mmHg';
        updateChart(time, systolic, diastolic);
        updateReading(bp, pulse + 'bpm', spo2 + '%');
      }, 5000); // update every 5 seconds
