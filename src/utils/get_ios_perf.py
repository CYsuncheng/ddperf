import sys
import time

import tidevice
import json
import requests

bundle_id = "com.luojilab.LuoJiFM-IOS"
udid = "00008101-001A6DD01A69003A"

dev = "http://192.168.128.12:5000"
pro = "https://backend.luojilab.com"

add_perf_info = "/performance/addperfinfo"
request_data = {
    "version": "",
    "platform": "",
    "device": "",
    "mem": "",
    "cpu": "",
    "fps": ""
}


class UploadPerfResult(object):

    @staticmethod
    def get_request_data(version, platform, device, mem, cpu, fps):
        request_data["version"] = version
        request_data["platform"] = platform
        request_data["device"] = device
        request_data["mem"] = mem
        request_data["cpu"] = cpu
        request_data["fps"] = fps
        return json.dumps(request_data)

    @staticmethod
    def upload_perf_data(version, platform, device, mem, cpu, fps, domain):
        global r
        if domain == "dev":
            r = requests.post(url=dev + add_perf_info,
                              data=UploadPerfResult.get_request_data(version, platform, device, mem, cpu, fps))
        elif domain == "pro":
            r = requests.post(url=pro + add_perf_info,
                              data=UploadPerfResult.get_request_data(version, platform, device, mem, cpu, fps))
        return r.text


class GetiOSPerf(object):
    t = tidevice.Device(udid=udid)
    perf = tidevice.Performance(t, perfs=list(tidevice.DataType))
    perf_value = {
        "cpu": "",
        "memory": ""
    }

    @staticmethod
    def callback_get(_type: tidevice.DataType, value: dict, version: str):
        if _type.value == "cpu":
            ss = str(value)  # 转成str
            use_cpu = ss.split("'value':")[1][0:6].split("}")[0]
            sys_cpu = ss.split("'sys_value':")[1][0:7].split("}")[0]
            count_cpu = ss.split("'count':")[1].split("}")[0]
            GetiOSPerf.perf_value["cpu"] = use_cpu

        if _type.value == "memory":
            ss = str(value)
            memory = ss.split("'value':")[1][0:6].split("}")[0]
            GetiOSPerf.perf_value["memory"] = memory
            print(GetiOSPerf.perf_value)
            if GetiOSPerf.perf_value["memory"] != "":
                UploadPerfResult.upload_perf_data(version=version, platform="iOS",
                                                  device="iPhone 12mini", mem=GetiOSPerf.perf_value["memory"],
                                                  cpu=GetiOSPerf.perf_value["cpu"],
                                                  fps=0, domain="dev")


if __name__ == '__main__':
    version = sys.argv[1]
    GetiOSPerf.perf.start(bundle_id=bundle_id, callback=GetiOSPerf.callback_get(version=version))
    time.sleep(120)
    GetiOSPerf.perf.stop()
