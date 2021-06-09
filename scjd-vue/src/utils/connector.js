import axios from "axios";

const baseurl = "http://10.128.249.37:8000";

export async function getPatentPie(){
    var info = undefined
    await axios.get(`${baseurl}/patent-pie/`)
            .then(function(response){
                info = response.data;
            })
            .catch(function (error) {
                console.log(error);
            })
    return info
}