import axios from "axios";

export const baseurl = "http://10.112.207.130:14144";

export async function getLayout() {
    const response = await axios.get(`${baseurl}/chart-data/display`);
    const layout = response.data.layout.map(item => {
      return {
        x: item.x_coordinate,
        y: item.y_coordinate,
        w: item.width,
        h: item.height,
        i: item.id
      }
    });
    console.log(layout)
    return layout;
}

export async function getCardByID(itemID) {
    const response = await axios.get(`${baseurl}/chart-data/charts/${itemID}/?fields=name,type,history`);
    return {
      type: response.data.type,
      name: response.data.name,
      info: response.data.history.file_url
    };
}

export async function updateLayout(layout) {
  const response = await axios.put(`${baseurl}/chart-data/display`, 
    layout.map(item => {
      return {
        id: item.id,
        x_coordinate: item.x,
        y_coordinate: item.y,
        width: item.w,
        height: item.h
      }
    })
  );
  if(response.data.length === layout.length){
    return "success"
  }
}

export async function getDataList(){
  const response = await axios.get(`${baseurl}/chart-data/charts/?fields=id,name`);
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
      timestamp: item.timestamp,
      file_url: item.file_url
    }
  });
}

export async function newDataItem(itemName){
  const response = await axios.post(`${baseurl}/chart-data/charts/`, {
    name: itemName,
  })
  if(response.status === 201){
    console.log(response)
    return response.data.id
  } 
}