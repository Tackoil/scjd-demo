import {baseurl} from "@/utils/connector.js"

/*
function getUrlSingleParam(key, url = location.search){
	const reg = new RegExp("(\\?|&)" + key + "=([^&]*)(&|$)");
	const r = url.match(reg);
	if (r != null) {
		return unescape(r[2]);
	}
	return null;
}
*/

let Mock = require('mockjs')
let Random = Mock.Random

const xj_place = [
    "乌鲁木齐",
    "昌吉州",
    "克拉玛依",
    "石河子",
    "伊犁州",
    "博州",
    "塔城",
    "阿勒泰",
    "吐鲁番",
    "哈密",
    "巴州",
    "阿克苏",
    "喀什",
    "和田",
    "克州"
]

const time_x_label = [
    "2020.01", "2020.02", "2020.03", "2020.04", "2020.05", "2020.06",
    "2020.07", "2020.08", "2020.09", "2020.10", "2020.11", "2020.12"
]

Mock.setup({
    timeout: '200-600'
})

Mock.mock(`${baseurl}/chart-data/display/`, "get", function(){
    return {
        layout: [
            { "x_coordinate": 0, "y_coordinate": 0, "width": 7, "height": 9, "id": 0 },
            { "x_coordinate": 0, "y_coordinate": 9, "width": 7, "height": 9, "id": 1 },
            { "x_coordinate": 12, "y_coordinate": 0, "width": 4, "height": 7, "id": 2 },
            { "x_coordinate": 11, "y_coordinate": 14, "width": 5, "height": 8, "id": 3 },
            { "x_coordinate": 0, "y_coordinate": 18, "width": 7, "height": 8, "id": 4 },
            { "x_coordinate": 7, "y_coordinate": 14, "width": 4, "height": 8, "id": 5 },
            { "x_coordinate": 7, "y_coordinate": 7, "width": 9, "height": 6, "id": 6 },
            { "x_coordinate": 7, "y_coordinate": 0, "width": 5, "height": 7, "id": 7 },
        ]
    }
}
)

Mock.mock(new RegExp(`${baseurl}/chart-data/charts/[0-9]+/\\?fields=name,type,history/`), "get",
    function(options){
        console.log('did', options.url)
        //const itemID = getUrlSingleParam("itemID", options.url)
        const itemID = options.url.split('/')[5]
        console.log("mock getCardByID", itemID)
        return {
            0: {
                type: 0,
                name: "2021年2月新疆专利授权状况统计",
                history: {
                    timestamp: 1627957218000,
                    file_url: {
                        "num_patent_types": Array.apply(null, new Array(3)).map(() => Random.natural(50, 100)),
                        "num_applicants_types":  Array.apply(null, new Array(5)).map(() => Random.natural(80, 100))
                    }
                }
            },
            1: {
                type: 1,
                name: "2020年各地州专利授权状况年累计变化",
                history: {
                    timestamp: 1627957218000,
                    file_url: {
                        "time_x_label": time_x_label,
                        "sum": xj_place.map(item => {
                            return {
                                name: item,
                                data: Array.apply(null, new Array(12)).map(() => Random.natural(100, 5000))
                            }
                        })
                    }  
                }
            },
            2: {
                type: 2,
                name: "新疆三种专利每月申请受理趋势变化",
                history: {
                    timestamp: 1627957218000,
                    file_url: {
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
                                ["发明专利", ...Array.apply(null, new Array(6)).map(() => Random.natural(0, 1000))],
                                ["实用新型", ...Array.apply(null, new Array(6)).map(() => Random.natural(0, 1000))],
                                ["外观设计", ...Array.apply(null, new Array(6)).map(() => Random.natural(0, 1000))],
                            ],
                        },
                    }
                }
            },
            3: {
                type: 3,
                name: "2021年2月新疆各地州专利授权情况",
                history: {
                    timestamp: 1627957218000,
                    file_url: {
                        num: xj_place.map(place => {
                            return {
                                name: place,
                                value: Random.natural(0, 500)
                            }
                        })
                    }
                }
            },
            4: {
                type: 7,
                name: "市场监督新闻动态",
                history: {
                    timestamp: 1627957218000,
                    file_url: [
                            "工作", 
                            "发展", 
                            "质量", 
                            "文化", 
                            "党史", 
                            "企业", 
                            "学习", 
                            "会议", 
                            "润疆", 
                            "质量奖",
                            "教育", 
                            "气象", 
                            "开展", 
                            "坚持", 
                            "深入", 
                            "能源", 
                            "服务", 
                            "组织"
                    ].map(item => [item, Random.natural(1, 80)])
                }
            },
            5: {
                type: 5,
                name: "各行业企业分布情况",
                history: {
                    timestamp: 1627957218000,
                    file_url: [
                        "批发和零售业",
                        "租赁和商务服务业",
                        "建筑业",
                        "制造业",
                        "科学研究和技术服务业",
                        "农、林、牧、渔业",
                        "信息运输、电子软件业",
                        "房地产业",
                        "交通运输、仓储和邮政业",
                        "文化、体育和娱乐业",
                        "金融业",
                        "其他"
                    ].map(item => {
                        return {value: Random.natural(800, 5000), name: item}
                    })
                }
            },
            6: {
                type: 6,
                name: "企业注册、变更、注销统计",
                history: {
                    timestamp: 1627957218000,
                    file_url: {
                        "time_x_label": time_x_label,
                        "sum": ["注册", "变更", "注销"].map(item => {
                            return {name: item, data: Array.apply(null, new Array(12)).map(() => Random.natural(100, 7000))}
                        })
                    }
                }
            },
            7: {
                type: 4,
                name: "市场主体产业数目变化",
                history: {
                    timestamp: 1627957218000,
                    file_url: {
                        "time_x_label": time_x_label,
                        "sum": ["第一产业", "第二产业", "第三产业"].map(item => {
                            return {
                                name: item,
                                data: Array.apply(null, new Array(12)).map(() => Random.natural(100, 7000))
                            }
                        })
                    }
                }
            }
        }[itemID]
    }
)

Mock.mock(`${baseurl}/chart-data/charts/?fields=id,name/`, "get", function(){
    console.log("mock getDataList")
    return [
        {
            "id": 6, 
            "name": "测试图表1" 
        },
        {
            "id": 7, 
            "name": "测试图表2_更新测试_PATCH" 
        },
        {
            "id": 11, 
            "name": "上传测试图表" 
        },
        {
            "id": 13, 
            "name": "删除测试图表2" 
        },
        {
            "id": 8, 
            "name": "测试图表3"   
        },
        {
            "id": 9, 
            "name": "测试图表4"  
        },
        {
            "id": 14, 
            "name": "自定义折线图图表测试" 
        }
    ]
})

Mock.mock(new RegExp(`${baseurl}/chart-data/charts/[0-9]+/\\?fields=id,name,history,type,display,removable/`), "get", 
    function(options){
        console.log('did', options.url)
        const itemID = options.url.split('/')[5]
        console.log("mock getDataItem", itemID)
        return {
            0: {
                type: 0,
                name: "2021年2月新疆专利授权状况统计",
                display: true,
                history: [
                    {
                        timestamp: 1627957218000,
                        file_url: {
                            "num_patent_types": Array.apply(null, new Array(3)).map(() => Random.natural(50, 100)),
                            "num_applicants_types":  Array.apply(null, new Array(5)).map(() => Random.natural(80, 100))
                        }
                    },
                    {
                        timestamp: 1627957219000,
                        file_url: {
                            "num_patent_types": Array.apply(null, new Array(3)).map(() => Random.natural(50, 100)),
                            "num_applicants_types":  Array.apply(null, new Array(5)).map(() => Random.natural(80, 100))
                        }
                    }
                ]
            },
            1: {
                type: 1,
                name: "2020年各地州专利授权状况年累计变化",
                history: {
                    timestamp: 1627957218000,
                    file_url: {
                        "time_x_label": time_x_label,
                        "sum": xj_place.map(item => {
                            return {
                                name: item,
                                data: Array.apply(null, new Array(12)).map(() => Random.natural(100, 5000))
                            }
                        })
                    }  
                }
            },
            2: {
                type: 2,
                name: "新疆三种专利每月申请受理趋势变化",
                history: {
                    timestamp: 1627957218000,
                    file_url: {
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
                                ["发明专利", ...Array.apply(null, new Array(6)).map(() => Random.natural(0, 1000))],
                                ["实用新型", ...Array.apply(null, new Array(6)).map(() => Random.natural(0, 1000))],
                                ["外观设计", ...Array.apply(null, new Array(6)).map(() => Random.natural(0, 1000))],
                            ],
                        },
                    }
                }
            },
            3: {
                type: 3,
                name: "2021年2月新疆各地州专利授权情况",
                history: {
                    timestamp: 1627957218000,
                    file_url: {
                        num: xj_place.map(place => {
                            return {
                                name: place,
                                value: Random.natural(0, 500)
                            }
                        })
                    }
                }
            },
            4: {
                type: 7,
                name: "市场监督新闻动态",
                history: {
                    timestamp: 1627957218000,
                    file_url: [
                            "工作", 
                            "发展", 
                            "质量", 
                            "文化", 
                            "党史", 
                            "企业", 
                            "学习", 
                            "会议", 
                            "润疆", 
                            "质量奖",
                            "教育", 
                            "气象", 
                            "开展", 
                            "坚持", 
                            "深入", 
                            "能源", 
                            "服务", 
                            "组织"
                    ].map(item => [item, Random.natural(1, 80)])
                }
            },
            5: {
                type: 5,
                name: "各行业企业分布情况",
                history: {
                    timestamp: 1627957218000,
                    file_url: [
                        "批发和零售业",
                        "租赁和商务服务业",
                        "建筑业",
                        "制造业",
                        "科学研究和技术服务业",
                        "农、林、牧、渔业",
                        "信息运输、电子软件业",
                        "房地产业",
                        "交通运输、仓储和邮政业",
                        "文化、体育和娱乐业",
                        "金融业",
                        "其他"
                    ].map(item => {
                        return {value: Random.natural(800, 5000), name: item}
                    })
                }
            },
            6: {
                type: 6,
                name: "企业注册、变更、注销统计",
                history: {
                    timestamp: 1627957218000,
                    file_url: {
                        "time_x_label": time_x_label,
                        "sum": ["注册", "变更", "注销"].map(item => {
                            return {name: item, data: Array.apply(null, new Array(12)).map(() => Random.natural(100, 7000))}
                        })
                    }
                }
            },
            7: {
                type: 4,
                name: "市场主体产业数目变化",
                history: {
                    timestamp: 1627957218000,
                    file_url: {
                        "time_x_label": time_x_label,
                        "sum": ["第一产业", "第二产业", "第三产业"].map(item => {
                            return {
                                name: item,
                                data: Array.apply(null, new Array(12)).map(() => Random.natural(100, 7000))
                            }
                        })
                    }
                }
            }
        }[itemID]
    }
)