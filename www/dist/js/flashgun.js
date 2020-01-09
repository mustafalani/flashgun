function ListServer() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        let parser;
        let xmlDoc;
        if (this.readyState == 4 && this.status == 200) {
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(this.responseText, "text/xml");
            let key ="";
            let value ="";
            let htmll ="";
            console.log(xmlDoc);
            console.log(xmlDoc.getElementsByTagName("ServerDetails"));
            for (let i = 0; i < xmlDoc.getElementsByTagName("ServerDetails")[0].children.length; i++) {
                for (let j = 0; j < xmlDoc.getElementsByTagName("ServerDetails")[0].children[i].attributes.length; j++) {
                    htmll += xmlDoc.getElementsByTagName("ServerDetails")[0].children[i].attributes[j].nodeName + " : " + xmlDoc.getElementsByTagName("ServerDetails")[0].children[i].attributes[j].nodeValue;
                    htmll += " ";
                }
            }
                document.getElementById("ListServer").innerHTML = htmll;
            }
        }

    xhttp.open("GET", "http://localhost:5000/api/v1/ListServer", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send("");
}


function ListWatchFolder() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        let parser;
        let xmlDoc;
        if (this.readyState == 4 && this.status == 200) {
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(this.responseText, "text/xml");
            let key ="";
            let value ="";
            let htmll ="";
            console.log(xmlDoc);
            console.log(xmlDoc.getElementsByTagName("WatchFolderDetails"));
            for (let i = 0; i < xmlDoc.getElementsByTagName("WatchFolderDetails")[0].children.length; i++) {
                for (let j = 0; j < xmlDoc.getElementsByTagName("WatchFolderDetails")[0].children[i].attributes.length; j++) {
                    htmll += xmlDoc.getElementsByTagName("WatchFolderDetails")[0].children[i].attributes[j].nodeName + " : " + xmlDoc.getElementsByTagName("WatchFolderDetails")[0].children[i].attributes[j].nodeValue;
                    htmll += " ";
                }
            }
                document.getElementById("ListWatchFolder").innerHTML = htmll;
            }
        }

    xhttp.open("GET", "http://localhost:5000/api/v1/ListWatchFolder", true);

    xhttp.send("");
}


function ListRestoreFolder() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        let parser;
        let xmlDoc;
        if (this.readyState == 4 && this.status == 200) {
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(this.responseText, "text/xml");
            let key ="";
            let value ="";
            let htmll ="";
            console.log(xmlDoc);
            console.log(xmlDoc.getElementsByTagName("RestoreFolderDetails"));
            for (let i = 0; i < xmlDoc.getElementsByTagName("RestoreFolderDetails")[0].children.length; i++) {
                for (let j = 0; j < xmlDoc.getElementsByTagName("RestoreFolderDetails")[0].children[i].attributes.length; j++) {
                    htmll += xmlDoc.getElementsByTagName("RestoreFolderDetails")[0].children[i].attributes[j].nodeName + " : " + xmlDoc.getElementsByTagName("RestoreFolderDetails")[0].children[i].attributes[j].nodeValue;
                    htmll += "<br> ";
                }
            }
                document.getElementById("ListRestoreFolder").innerHTML = htmll;
            }
        }

    xhttp.open("GET", "http://localhost:5000/api/v1/ListRestoreFolder", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send("");
}


function SearchArchive() {
    let xhttp = new XMLHttpRequest();
    let assets = document.getElementById("search-assets").placeholder;
    let searchdata = {};
    searchdata.Guid = assets;
    searchdata.Group  = "%";
    searchdata.Volume  = "%";
    searchdata.ArchivedFromDate  = "*";
    searchdata.ArchivedToDate  = "*";
    searchdata.DeletedFromDate  = "*";
    searchdata.DeletedToDate  = "*";
    searchdata.PageSize  = "100";
    searchdata.FromQWD  = "0";
    searchdata.FlagsDWD  = "0";
    searchdata.IncludeMetadataDWD  = "0";
    let searchjson = JSON.stringify(searchdata);
    xhttp.onreadystatechange = function() {
        let parser;
        let xmlDoc;
        if (this.readyState == 4 && this.status == 200) {
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(this.responseText, "text/xml");
            let key ="";
            let value ="";
            let htmll ="";
            console.log(xmlDoc);
            console.log(xmlDoc.getElementsByTagName("FileDetails"));
            for (let i = 0; i < xmlDoc.getElementsByTagName("FileDetails")[0].children.length; i++) {
                for (let j = 0; j < xmlDoc.getElementsByTagName("FileDetails")[0].children[i].attributes.length; j++) {
                    htmll += xmlDoc.getElementsByTagName("FileDetails")[0].children[i].attributes[j].nodeName + " : " + xmlDoc.getElementsByTagName("FileDetails")[0].children[i].attributes[j].nodeValue;
                    htmll += "<br> ";
                }
            }
                document.getElementById("SearchArchive").innerHTML = htmll;
            }
        }

    xhttp.open("GET", "http://localhost:5000/api/v1/SearchArchive", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(JSON.stringify(searchdata));
    console.log(searchjson);
}