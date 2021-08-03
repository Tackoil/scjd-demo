import axios from "axios";

export const baseurl = "http://10.128.232.15:8000";

export async function getLayout() {
  const response = await axios.get(`${baseurl}/getLayout/`)
  const layout = response.data.layout;
  return {layout: layout};
}

export async function getCardByID(itemID) {
  const response = await axios
    .get(`${baseurl}/getCardByID/`, {
      params: {
        itemID: itemID,
      },
    })
  return response.data;
}
