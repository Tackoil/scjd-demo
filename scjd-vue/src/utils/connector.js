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

export async function getPatentLineRace(){
    var info = undefined
    await axios.get(`${baseurl}/patent-line-race/`)
            .then(function(response){
                info = response.data;
            })
            .catch(function (error) {
                console.log(error);
            })
    return info
}


export async function getPatentLine(){
    var info = undefined
    await axios.get(`${baseurl}/patent-line/`)
            .then(function(response){
                info = response.data;
            })
            .catch(function (error) {
                console.log(error);
            })
    return info
}


export async function getPatentMap(){
    var info = undefined
    await axios.get(`${baseurl}/patent-map/`)
            .then(function(response){
                info = response.data;
            })
            .catch(function (error) {
                console.log(error);
            })
    return info
}


export async function getNewsWordMap(){
    var info = undefined
    await axios.get(`${baseurl}/news-word-map/`)
            .then(function(response){
                info = response.data;
            })
            .catch(function (error) {
                console.log(error);
            })
    return info
}

export async function getEnterpriseBar(){
    var info = undefined
    await axios.get(`${baseurl}/enterprise-bar/`)
            .then(function(response){
                info = response.data;
            })
            .catch(function (error) {
                console.log(error);
            })
    return info
}

export async function getEpAlterLine(){
    var info = undefined
    await axios.get(`${baseurl}/ep-alter-line/`)
            .then(function(response){
                info = response.data;
            })
            .catch(function (error) {
                console.log(error);
            })
    return info
}

export async function getEpDistributionPie(){
    var info = undefined
    await axios.get(`${baseurl}/ep-distribution-pie/`)
            .then(function(response){
                info = response.data;
            })
            .catch(function (error) {
                console.log(error);
            })
    return info
}