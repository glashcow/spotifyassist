document.addEventListener('DOMContentLoaded', () => {
    
    document.querySelectorAll('.list-link').forEach(link => {
        link.onclick = () => {
            const artistlist = link.dataset.artistlist;
            document.querySelector('#artistlistlist').style.display = 'none';
            document.querySelector('#specificlist').style.display = 'block';
            loadlist(artistlist);
            return false;
        };
    });
    
    document.querySelector('#addlist').onsubmit = function() {
        var listname = document.querySelector('#newlistquery').value;
        newlist(listname)
        return false;
    };
});


function newlist(listname) {
    const request = new XMLHttpRequest();
    request.open('GET', `/newlist/${listname}`);
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        document.querySelector('#listmessage').innerHTML = data.message;
        if(data.good === "good"){
            return true;
        }
        else{
            return false;
        }
    };
    request.send();
}


function loadlist(artistlist) {
    const request = new XMLHttpRequest();
    request.open('GET', `/loadlist/${artistlist}`);
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        for(var i = 0; i < data.artists.length ; i++ ){
            const li = document.createElement('li');         
            li.innerHTML = data.artists[i];
            li.classList.add("artistinlist");
            (function(artist, list){
                li.addEventListener("click", function() {
                    deleteArtist(artist, list);
            }, false);})(data.artists[i], artistlist);
            document.querySelector('#specificlist').append(li);  
        }
        const back = document.createElement('button'); 
            (function(){
                back.addEventListener("click", function() {
                    backToLists();
            }, false);}());
            back.innerHTML = "&#8249; Back To Lists";
            document.querySelector('#specificlist').append(back);
    };
    request.send();
}
    
    
function deleteArtist(artist, artistlist){
    const request = new XMLHttpRequest();
    request.open('GET', `/removeartist/${artistlist}/${artist}`);
    request.onload = () => {
        document.querySelector('#specificlist').innerHTML = "";
        const data = JSON.parse(request.responseText);
        for(var i = 0; i < data.artists.length ; i++ ){
            const li = document.createElement('li');         
            li.innerHTML = data.artists[i];
            li.classList.add("artistinlist");
            (function(artist, list){
                li.addEventListener("click", function() {
                    deleteArtist(artist, list);
            }, false);})(data.artists[i], artistlist);
            document.querySelector('#specificlist').append(li);
        }
        const back = document.createElement('button'); 
            (function(){
                back.addEventListener("click", function() {
                    backToLists();
            }, false);}());
            back.innerHTML = "&#8249; Back To Lists";
            document.querySelector('#specificlist').append(back);
    };
    request.send();
}

function backToLists() {
    document.querySelector('#specificlist').innerHTML = "";
    document.querySelector('#artistlistlist').style.display = 'block';
    document.querySelector('#specificlist').style.display = 'none';
}