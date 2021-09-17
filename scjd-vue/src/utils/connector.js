import axios from "axios";

export const baseurl = "http://10.112.207.130:14144";

export async function getLayout() {
    const response = await axios.get(`${baseurl}/chart-data/display`);
    const layout = response.data.map(item => {
      return {
        x: item.x_coordinate,
        y: item.y_coordinate,
        w: item.width,
        h: item.height,
        i: item.id,
          minW: item.min_width,
          minH: item.min_height
      }
    });
    console.log(layout)
    return layout;
}

export async function getCardByID(itemID) {
    const response = await axios.get(`${baseurl}/chart-data/charts/${itemID}/?fields=name,type,history`);
    const parseHistory = await getDataParse(itemID, response.data.history.timestamp)
    return {
      type: response.data.type,
      name: response.data.name,
      info: parseHistory
    };
}

export async function updateLayout(layout, deleteList=[]) {
  const response = await axios.put(`${baseurl}/chart-data/display/`,
    layout.map(item => {
      return {
        id: item.i,
        x_coordinate: item.x,
        y_coordinate: item.y,
        width: item.w,
        height: item.h,
          display: deleteList.indexOf(item.i) === -1
      }
    })
  );
  if(response.data.length === layout.length){
    return "success"
  }
}

export async function getDataList(){
  const response = await axios.get(`${baseurl}/chart-data/charts/?fields=id,name,display`);
  const datalist = response.data;
  console.log(datalist)
  return datalist;
}

export async function getDataItem(itemID){
  const response = await axios.get(`${baseurl}/chart-data/charts/${itemID}/?fields=id,name,history,type,display,removable`);
  return {
    id: response.data.id,
    name: response.data.name,
    type: response.data.type,
    display: response.data.display,
    removable: response.data.removable,
    history: response.data.history
  };
}

export async function getDataItemHistory(itemID){
  const response = await axios.get(`${baseurl}/chart-data/files/?chart=${itemID}`);
  return response.data.map(item => {
    return {
        id: item.id,
      timestamp: item.timestamp,
      file_url: item.file_url
    }
  });
}

export async function newDataItem(itemName){
  const response = await axios.post(`${baseurl}/chart-data/charts/`, {
    name: itemName,
    removable: true
  })
  if(response.status === 201){
    console.log(response)
    return response.data.id
  } 
}

export function downloadDatafileUrl(chartID, timestamp){
  return `${baseurl}/chart-data/files/download/?chart=${chartID}&timestamp=${timestamp}`
}

export async function deleteDataItem(itemID){
  const response = await axios.delete(`${baseurl}/chart-data/charts/${itemID}/`,
      {
        validateStatus: function (status) {
          return status < 500; // 处理状态码小于500的情况
        }
      })
  if(response.status !== 204){
    return {
      code: -1,
      msg: response.data.message
    }
  } else {
    return {
      code: 0,
      msg: "已成功删除"
    }
  }
}

export async function newUploadData(chartId, timestamp, file){
    const formdata = new FormData();
    formdata.append("chart", chartId)
    formdata.append("timestamp", timestamp)
    formdata.append("file_url", file)
    const response = await axios.post(`${baseurl}/chart-data/files/`, formdata, {
        headers: {
            "Content-Type": "multipart/form-data"
        }
    })
    return response
}

export async function replaceUploadData(uploadId, file){
    const formdata = new FormData();
    formdata.append("file_url", file)
    const response = await axios.patch(`${baseurl}/chart-data/files/${uploadId}/`, formdata, {
        headers: {
            "Content-Type": "multipart/form-data"
        }
    })
    return response
}

export async function getDataParse(chartID, timestamp){
  const response = await axios.get(`${baseurl}/chart-data/files/parse/?chart=${chartID}&timestamp=${timestamp}`,
      {
        validateStatus: function (status) {
          return status < 500; // 处理状态码小于500的情况
        }
      })
  return response.data;
}

export async function updateDataItem(itemID, data){
    const response = await axios.put(`${baseurl}/chart-data/charts/${itemID}/`, {
        display: data.display,
        name: data.name,
        type: data.type,
        width: data.w,
        height: data.h,
        min_width: data.minw,
        min_height: data.minh
    })
    return response.data
}
