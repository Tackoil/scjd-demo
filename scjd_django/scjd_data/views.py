import json
import random

from django.http import HttpResponse


def random_distort(res):
    if isinstance(res, dict):
        for key in res:
            res[key] = random_distort(res[key])
    elif isinstance(res, list):
        for item in range(len(res)):
            res[item] = random_distort(res[item])
    elif isinstance(res, int):
        delta_max = int(res * 0.3)
        res = res + random.randint(-1 * delta_max, delta_max)
    return res


def patent_pie(request):
    if request.method == 'GET':
        res = {
            "num_patent_types": [84, 901, 52],
            "num_applicants_types": [262, 546, 134, 55, 40],
        }
        res = random_distort(res)
        res = json.dumps(res)
        return HttpResponse(res)


def patent_line_race(request):
    if request.method == 'GET':
        res = {
            "time_x_label": [
                "2020.01",
                "2020.02",
                "2020.03",
                "2020.04",
                "2020.05",
                "2020.06",
                "2020.07",
                "2020.08",
                "2020.09",
                "2020.10",
                "2020.11",
                "2020.12",
            ],
            "sum": [
                {
                    "name": "乌鲁木齐",
                    "data": [
                        1000, 1100, 1400, 1400, 2000, 2400, 3000, 3000, 4000, 4766,
                        5315, 5332,
                    ],
                },
                {
                    "name": "昌吉州",
                    "data": [
                        100, 110, 140, 170, 200, 240, 300, 350, 400, 476, 531, 533,
                    ],
                },
                {
                    "name": "克拉玛依",
                    "data": [
                        55, 102, 138, 188, 246, 313, 386, 413, 457, 473, 556, 646,
                    ],
                },
                {
                    "name": "石河子",
                    "data": [
                        20, 109, 114, 192, 208, 271, 307, 339, 350, 399, 498, 523,
                    ],
                },
                {
                    "name": "伊犁州",
                    "data": [
                        35, 95, 141, 229, 261, 354, 396, 396, 403, 481, 518, 558,
                    ],
                },
                {
                    "name": "博州",
                    "data": [
                        69, 96, 116, 210, 280, 301, 360, 397, 413, 489, 570, 639,
                    ],
                },
                {
                    "name": "塔城",
                    "data": [
                        69, 96, 116, 210, 280, 301, 360, 397, 413, 489, 570, 639,
                    ],
                },
                {
                    "name": "阿勒泰",
                    "data": [25, 65, 82, 121, 129, 155, 159, 168, 195, 209, 209, 226],
                },
                {
                    "name": "吐鲁番",
                    "data": [
                        69, 96, 116, 210, 280, 301, 360, 397, 413, 489, 570, 639,
                    ],
                },
                {
                    "name": "哈密",
                    "data": [1, 19, 21, 35, 52, 59, 67, 84, 86, 100, 117, 136],
                },
                {
                    "name": "巴州",
                    "data": [1, 19, 21, 35, 52, 59, 67, 84, 86, 100, 117, 136],
                },
                {
                    "name": "阿克苏",
                    "data": [25, 65, 82, 121, 129, 155, 159, 168, 195, 209, 209, 226],
                },
                {
                    "name": "喀什",
                    "data": [
                        69, 96, 116, 210, 280, 301, 360, 397, 413, 489, 570, 639,
                    ],
                },
                {
                    "name": "和田",
                    "data": [1, 19, 21, 35, 52, 59, 67, 84, 86, 100, 117, 136],
                },
                {
                    "name": "克州",
                    "data": [1, 19, 21, 35, 52, 59, 67, 84, 86, 100, 117, 136],
                },
            ],
        }
        res = random_distort(res)
        res = json.dumps(res)
        return HttpResponse(res)


def patent_line(request):
    if request.method == 'GET':
        res = {
            "dataset": {
                "source": [
                    [
                        "Proportion",
                        "2020.10",
                        "2020.11",
                        "2020.12",
                        "2021.01",
                        "2021.02",
                        "2021.03",
                    ],
                    ["发明专利", 326, 468, 92, 59, 84, 102],
                    ["实用新型", 1390, 1670, 1077, 865, 901, 1196],
                    ["外观设计", 91, 91, 79, 50, 52, 133],
                ],
            },
        }
        res = random_distort(res)
        res = json.dumps(res)
        return HttpResponse(res)


def patent_map(request):
    if request.method == "GET":
        res = {
            "num": [
                {"name": "乌鲁木齐", "value": 507},
                {"name": "昌吉州", "value": 61},
                {"name": "克拉玛依", "value": 44},
                {"name": "石河子", "value": 70},
                {"name": "伊犁州", "value": 65},
                {"name": "博州", "value": 16},
                {"name": "塔城", "value": 30},
                {"name": "阿勒泰", "value": 14},
                {"name": "吐鲁番", "value": 32},
                {"name": "哈密", "value": 71},
                {"name": "巴州", "value": 47},
                {"name": "阿克苏", "value": 62},
                {"name": "喀什", "value": 36},
                {"name": "和田", "value": 9},
                {"name": "克州", "value": 4},
            ],
        }
        res = random_distort(res)
        res = json.dumps(res)
        return HttpResponse(res)


def news_word_map(request):
    if request.method == "GET":
        res = [
            ["工作", 76],
            ["发展", 68],
            ["质量", 61],
            ["文化", 56],
            ["党史", 48],
            ["企业", 47],
            ["学习", 46],
            ["会议", 44],
            ["润疆", 43],
            ["质量奖", 39],
            ["教育", 37],
            ["气象", 34],
            ["开展", 32],
            ["坚持", 28],
            ["深入", 26],
            ["能源", 25],
            ["服务", 25],
            ["组织", 25],
        ]
        res = random_distort(res)
        res = json.dumps(res)
        return HttpResponse(res)


def enterprise_bar(request):
    if request.method == "GET":
        res = {
            "time_x_label": [
                "2020.01", "2020.02", "2020.03", "2020.04", "2020.05", "2020.06",
                "2020.07", "2020.08", "2020.09", "2020.10", "2020.11", "2020.12"
            ],
            "sum": [
                {
                    "name": "第一产业",
                    "data": [1036, 1748, 1915, 2519, 2865, 2962,
                             3693, 3810, 4298, 4323, 4675, 6209],
                },
                {
                    "name": "第二产业",
                    "data": [209, 317, 533, 844, 1019, 1155,
                             1484, 1610, 2285, 2772, 3578, 4308],
                },
                {
                    "name": "第三产业",
                    "data": [204, 220, 327, 381, 482, 507,
                             800, 951, 1001, 1200, 1390, 1776],
                },
            ],
        }
        res = random_distort(res)
        res = json.dumps(res)
        return HttpResponse(res)


def ep_alter_line(request):
    if request.method == "GET":
        res = {
            "time_x_label": [
                "2020.01", "2020.02", "2020.03", "2020.04", "2020.05", "2020.06",
                "2020.07", "2020.08", "2020.09", "2020.10", "2020.11", "2020.12"
            ],
            "sum": [
                {
                    "name": "注册",
                    "data": [1036, 1748, 1915, 2519, 2865, 2962,
                             3693, 3810, 4298, 4323, 4675, 6209, ],
                },
                {
                    "name": "变更",
                    "data": [1155, 844, 2285, 2772, 317, 533,
                             1610, 209, 3578, 1484, 4308, 1019],
                },
                {
                    "name": "注销",
                    "data": [482, 220, 1200, 381, 951, 1001,
                             204, 1390, 507, 800, 1776, 327,
                             ],
                },
            ],
        }
        res = random_distort(res)
        res = json.dumps(res)
        return HttpResponse(res)


def ep_distribution_pie(request):
    if request.method == "GET":
        res = [
            {"value": 42176, "name": "批发和零售业"},
            {"value": 31663, "name": "租赁和商务服务业"},
            {"value": 28685, "name": "建筑业"},
            {"value": 23703, "name": "制造业"},
            {"value": 22393, "name": "科学研究和技术服务业"},
            {"value": 18358, "name": "农、林、牧、渔业"},
            {"value": 16920, "name": "信息运输、电子软件业"},
            {"value": 10095, "name": "房地产业"},
            {"value": 9910, "name": "交通运输、仓储和邮政业"},
            {"value": 7221, "name": "文化、体育和娱乐业"},
            {"value": 7154, "name": "金融业"},
            {"value": 5930, "name": "其他"},
        ]
        res = random_distort(res)
        res = json.dumps(res)
        return HttpResponse(res)
