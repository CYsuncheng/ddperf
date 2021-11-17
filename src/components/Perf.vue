<template>
  <div>
    <div id="container" style="min-width: 400px; height: 400px">
    </div>
    <button v-if="!start_perf" v-on:click="changeButton()" v-text="button_text">
      {{ button_text }}
    </button>
    <button v-else v-on:click="changeButton()" v-text="button_text">
      {{ button_text }}
    </button>
  </div>
</template>

<script>
import Highcharts from "highcharts";
// import axios from "axios";

export default {
  name: "Perf",
  props: {},
  data() {
    return {
      Highcharts: Highcharts,
      title: "iOS 内存数据展示",
      start: false,
      button_text: "start",
      start_perf: false,
    };
  },
  watch: {
      start_perf: function() {
          if (this.start_perf) {
            alert("开始获取数据")
          }else {
            alert("暂停获取数据")
          }
      }
  },
  mounted() {
    this.lineChartOnTime();
  },
  created() {},
  updated() {},
  methods: {
    // 想用来控制图表绘制的开关，但是暂时不可用
    changeButton() {
      if (this.start_perf) {
        this.start_perf = false;
        this.button_text = "start";
      } else {
        this.start_perf = true;
        this.button_text = "stop";
      }
      console.log("this start" + this.start_perf);
    },

    // 实现调用python脚本
    execPy() {
      var exec = require("child_process").exec;
      var arg1 = "9.7.0";
      var filename = "test_py.py";
      exec(
        "python" + " " + filename + " " + arg1,
        function (err, stdout, stderr) {
          if (err) {
            console.log("stderr", err + stderr);
          }
          if (stdout) {
            console.log("stdout", stdout);
          }
        }
      );
    },

    // 绘制highchart图表
    lineChartOnTime() {
      // 在方法内部，直接使用this去访问全局的data里面定义的变量无法实现，需要设置一个变量指向this变量
      var that_vue = this;

      Highcharts.setOptions({
        global: {
          useUTC: false,
        },
      });
      function activeLastPointToolip(chart) {
        var points = chart.series[0].points;
        chart.tooltip.refresh(points[points.length - 1]);
      }
      Highcharts.chart("container", {
        chart: {
          type: "spline",
          marginRight: 10,
          zoomType: "x",
          events: {
            load: function () {
              var series = this.series[0],
                chart = this;
              activeLastPointToolip(chart);
              setInterval(function () {
                // if (that_vue.start_perf) {
                //   axios
                //     .post(
                //       "http://192.168.128.12:5000/performance/getperfinfo",
                //       {
                //         platform: "ios",
                //       }
                //     )
                //     .then(
                //       (response) => (this.info = response.data.result[0].mem)
                //     );
                //   console.log(this.info);
                // }
                var x = new Date().getTime(), // 当前时间
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
          type: "datetime",
          tickPixelInterval: 100,
          crosshair: true,
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
              var data = [],
                time = new Date().getTime(),
                i;
              for (i = -19; i <= 0; i += 1) {
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
