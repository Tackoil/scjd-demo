# 接口文档

## 前端页面需求

### 1 数据大屏

- 1.1 根据数据项目ID 获得样式编号与最新的history数据
- 1.2 获取数据大屏的当前状态：`[{x, y, w, h, i:项目ID}, ...]` 
- 1.3 更新数据大屏的当前状态：上传的数据：`[{x, y, w, h, i:项目ID}, ...]`

### 2 数据项目管理主页面

- 2.1 获取所有数据项目：`[{id, name}, ...]`
- 2.2 （选作）根据关键词筛选项目：传一个query，返回和2.1一致。 

### 3 数据项目管理详情页面

- 3.1 根据数据项目ID 获得数据项目详情：

  ```json
  {
  	"id": "123",
      "name": "A Name",
      "history": [
      	{"timestamp": "时间戳，一串数字", "json": "json文件的位置"},
  		//...
      ],
  	"type": 1, //图表类型编号，已有图表以现在的编号为准吧。
  	"display": true, //true为展示，false为不展示。新添加的放在左下角（也就是x=0，y为所有卡片的最低坐标。
  	"removable": false, //不可删除
  }
  ```

- 3.2 添加新数据项目：信息与3.1一致，没有ID
- 3.3 根据数据项目ID 删除数据项目：**务必**再做一次检查是否可以删除
- 3.4 根据数据项目ID 修改信息：信息与3.1一致。每次上传完整信息。（之后个别条目可能要支持部分修改）
- 3.5 根据数据项目ID 上传新数据内容：emmm 一个文件
- 3.6 根据数据项目ID和时间戳 下载数据内容： emmm 另一个文件

### 4 可变图表编辑页面

待定

## HTTP 接口