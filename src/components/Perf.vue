<template>
  <div>
    <!-- <canvas id="myChart"></canvas> -->
    <div id="container" style="min-width: 400px; height: 400px"></div>
    <button v-if="!start_perf" v-on:click="changeButton()" v-text="button_text">
      {{ button_text }}
    </button>
    <button v-else v-on:click="changeButton()" v-text="button_text">
      {{ button_text }}
    </button>
    <!-- <button v-on:click="execPy()">python</button> -->
  </div>
</template>

<script>
import Highcharts from "highcharts";
import Chart from "chart.js/auto";
import axios from "axios";

export default {
  name: "Perf",
  props: {},
  data() {
    return {
      Highcharts: Highcharts,
      title: "iOS 内存数据展示",
      start: false,
      button_text: "开始",
      start_perf: false,
    };
  },
  watch: {
    // start_perf: function () {
    //   if (this.start_perf) {
    //     alert("开始获取数据");
    //   } else {
    //     alert("暂停获取数据");
    //   }
    // },
  },
  mounted() {
    this.lineChartOnTime();
    // this.chartDemo();
  },
  created() {},
  updated() {},
  methods: {
    chartDemo() {
      // chartjs 实时图表
      let dataLabels = [
        "1h",
        "2h",
        "3h",
        "4h",
        "5h",
        "6h",
        "7h",
        "8h",
        "9h",
        "10h",
        "11h",
        "12h",
        "13h",
        "14h",
        "15h",
        "16h",
        "17h",
        "18h",
        "19h",
        "20h",
        "21h",
        "22h",
        "23h",
        "0h",
      ];
      let dataPV = [
        133058, 253219, 255194, 233058, 253219, 277318, 277714, 273337, 255194,
        277318, 277714, 273337, 233058, 253219, 277318, 253219, 277318, 277714,
        273337, 255194, 277714, 273337, 255194, 293058,
      ];
      let dataUV = [
        10651, 22039, 23955, 23754, 22664, 10651, 22039, 23765, 23955, 23754,
        22664, 23765, 23955, 23754, 22664, 10651, 22039, 23765, 10651, 22039,
        23765, 23955, 23754, 22664,
      ];

      let config = {
        type: "line",
        data: {
          labels: dataLabels,
          datasets: [
            {
              label: "PV",
              data: dataPV,
              backgroundColor: "rgb(255, 99, 132)",
              borderColor: "rgb(255, 99, 132)",
              fill: false,
            },
            {
              label: "UV",
              data: dataUV,
              backgroundColor: "rgb(75, 192, 192)",
              borderColor: "rgb(75, 192, 192)",
              fill: false,
            },
          ],
        },
        options: {
          responsive: true,
          title: {
            display: true,
            text: "PV/UV 实时统计",
          },
        },
      };

      let ctx = document.getElementById("myChart").getContext("2d");
      let chart = new Chart(ctx, config);

      setInterval(function () {
        if (config.data.datasets.length > 0) {
          let last = parseInt(dataLabels[dataLabels.length - 1]);
          let label = last + 1;
          if (last >= 23) {
            label = 0;
          }
          label = new Date().toLocaleTimeString("en-GB");

          dataLabels.push(label);
          dataPV.push(getRandomNum(200000, 300000));
          console.log(getRandomNum(200000, 300000));
          dataUV.push(getRandomNum(10000, 80000));
          console.log(getRandomNum(10000, 80000));

          dataLabels.shift();
          dataPV.shift();
          dataUV.shift();

          chart.update();
        }
      }, 1000);

      function getRandomNum(min, max) {
        let range = max - min;
        let rand = Math.random();
        let randNum = min + Math.round(rand * range);
        return randNum;
      }
    },
    // 想用来控制图表绘制的开关，但是暂时不可用
    changeButton() {
      if (this.start_perf) {
        this.start_perf = false;
        this.button_text = "开始";
      } else {
        this.start_perf = true;
        this.button_text = "暂停";
      }
      console.log("this start" + this.start_perf);
    },

    // 实现调用python脚本
    execPy() {
      // let callback = function({data, pythonpath}){
      //   console.log(data)
      //   console.log(pythonpath)
      // }
      // let jsexecpy = require("jsexecpy");
      // jsexecpy.runpath("src/utils/get_ios_perf.py",callback)
      const execFile = require("child_process");
      execFile.exec(
        "python3",
        ["src/utils/get_ios_perf.py"],
        (error, stdout, stderr) => {
          if (error) throw error;
          console.log(stdout + stderr);
        }
      );
    },

    // 绘制highchart图表
    lineChartOnTime() {
      // 在方法内部，直接使用this去访问全局的data里面定义的变量无法实现，需要设置一个变量指向this变量
      let that_vue = this;

      Highcharts.setOptions({
        global: {
          useUTC: false,
        },
      });
      function activeLastPointToolip(chart) {
        let points = chart.series[0].points;
        chart.tooltip.refresh(points[points.length - 1]);
      }
      function getNewMem() {
        axios
          .post("http://192.168.128.12:5000/performance/getperfinfo", {
            platform: "ios",
          })
          .then((response) => (this.info = response.data.result[0].mem));
        console.log(this.info);
      }
      Highcharts.chart("container", {
        chart: {
          type: "spline",
          marginRight: 10,
          zoomType: "x",
          events: {
            load: function () {
              let series = this.series[0],
                chart = this;
              activeLastPointToolip(chart);
              setInterval(function () {
                if (that_vue.start_perf) {
                  getNewMem();
                }
                let x = new Date().getTime(), // 当前时间
                  y = Math.random() * 100 + 300; // 更新数据
                if (that_vue.start_perf) {
                  series.addPoint([x, y], true, true);
                }
                activeLastPointToolip(chart);
              }, 1000);
            },
          },
        },
        title: {
          text: this.title,
        },
        xAxis: {
          title: {
            text: "Time",
          },
          type: "datetime",
          tickPixelInterval: 10,
          crosshair: true,
        },
        scrollbar: {
          enabled: true,
        },
        yAxis: {
          title: {
            text: "Memory",
          },
          alternateGridColor: "#FDFFD5",
          crosshair: true,
          max: 1000,
          min: 100,
          tickAmount: 10,
        },
        tooltip: {
          formatter: function () {
            return (
              "<b>" +
              this.series.name +
              "</b><br/>" +
              Highcharts.dateFormat("%Y-%m-%d %H:%M:%S", this.x) +
              "<br/>" +
              Highcharts.numberFormat(this.y, 2)
            );
          },
        },
        legend: {
          enabled: false,
        },
        series: [
          {
            name: "内存数据",
            data: (function () {
              // 生成随机值
              let data = [],
                time = new Date().getTime(),
                i;
              for (i = -49; i <= 0; i += 1) {
                data.push({
                  x: time + i * 1000,
                  y: Math.random(), // 当前数据点前的数据
                });
              }
              return data;
            })(),
          },
        ],
      });
    },
  },
};
</script>
