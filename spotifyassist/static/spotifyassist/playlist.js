document.addEventListener('DOMContentLoaded', () => {
    
    document.querySelector('#playlistGeneratorForm').onsubmit = function() {
        const list = document.querySelector('#formlist').value;
        const formartists = document.querySelector('#formartists').value;
        const formtype = document.querySelector('#formtype').value;
        const count = document.querySelector('#count').value;
        playlist(list, formartists, formtype, count);
        return false;  
    };
});



function playlist(list, formartists, formtype, count){
    const request = new XMLHttpRequest();
    request.open('GET', `/newplaylist/${list}/${formartists}/${formtype}/${count}`);
    request.onload = () => {
        if(document.querySelector('#makeplaylistbutton') === null){}
        else {
            document.querySelector('#makeplaylistbutton').remove();
        }
        const data = JSON.parse(request.responseText);
        document.querySelector('#generatedPlaylist').innerHTML = "";
        for(var i = 0; i < data.tracks.length ; i++ ){
            const li = document.createElement('li');         
            li.innerHTML = data.tracks[i];
            document.querySelector('#generatedPlaylist').append(li);
        }
        const button = document.createElement('button'); 
        (function(){
            button.addEventListener("click", function() {
                addPlaylist();
        }, false);}());
        button.innerHTML = "Add to your playlists";
        button.id = "makeplaylistbutton"
        document.querySelector('#playlistDisplay').append(button);
        
        const p = document.createElement('p');
        p.innerHTML = data.uris;
        p.id = "uris";
        p.style.display = "none";
        document.querySelector('#generatedPlaylist').append(p);
    };
    request.send();
}

function addPlaylist() {
    const uris = document.querySelector('#uris').innerHTML;
    const request = new XMLHttpRequest();
    request.open('GET', `/makeplaylist/${uris}`);
    request.onload = () => {
        document.querySelector('#generatedPlaylist').innerHTML = "Added To Your Playlists";
        document.querySelector('#makeplaylistbutton').remove();
    };
    request.send();
}