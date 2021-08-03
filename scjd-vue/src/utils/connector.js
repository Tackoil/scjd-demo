import axios from "axios";

export const baseurl = "http://10.128.232.15:8000";

export async function getLayout() {
    const response = await axios.get(`${baseurl}/chart-data/display/`);
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
    const response = await axios.get(`${baseurl}/chart-data/charts/${itemID}/?fields=name,type,history/`);
    return {
      type: response.data.type,
      name: response.data.name,
      info: response.data.history[0].json_url
    };
}
/*
export async function updateLayout() {
  try {
    const response = await axios.put(`${baseurl}/updateLayout`);
  }
  catch {
    console.error('error')
  }
}
*/