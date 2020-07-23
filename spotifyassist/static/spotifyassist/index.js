document.addEventListener('DOMContentLoaded', () =>{
    
    if(localStorage.getItem("artistlist") === null){
        localStorage.setItem("artistlist", "faves");
    }
        
    document.querySelector('#artistSearch').onsubmit = function() {
        const currentlist = localStorage.getItem("artistlist");
        document.querySelector('#currentList').innerHTML = `Click To Add to ${currentlist}`;
        var searchvalue = document.querySelector('#searchquery').value;
        artistSearch(searchvalue);
        return false;
    };
    
    document.querySelectorAll('.nav-link').forEach(link => {
        link.onclick = () => {
            const list = link.dataset.list;
            document.querySelector('#currentList').innerHTML = `Click To Add to ${list}`;
            localStorage.setItem("artistlist", list);
            return false;
        };
    });
    
});





function artistSearch(searchvalue) {
    const request = new XMLHttpRequest();
    request.open('GET', `/artistsearch/${searchvalue}`);
    request.onload = () => {
        document.querySelector('#artistSearchResults').innerHTML = ""; 
        const data = JSON.parse(request.responseText);
        for(var i = 0; i < data.artists.length ; i++ ){
            const li = document.createElement('li');         
            li.innerHTML = data.artists[i];
            li.classList.add("searchresult");
            (function(value, id){
                li.addEventListener("click", function() {
                    addToList(value, id);
            }, false);})(data.artists[i], data.ids[i]);
            const img = document.createElement('img');   
            if(data.images[i] === "None"){
                img.src = "https://image.shutterstock.com/image-vector/no-image-available-sign-internet-600w-261719003.jpg"
            }
            else{
                img.src = data.images[i];    
            }
            img.style = "width:100px; height:100px; float:right; "
            li.append(img);
            document.querySelector('#artistSearchResults').append(li);     
        }
    };
    request.send();
}



function addToList(artist, id) {
    const request = new XMLHttpRequest();
    const list = localStorage.getItem("artistlist")
    request.open('GET', `/addtolist/${list}/${artist}/${id}`);
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        let message = data.message;
        document.querySelector('#message').innerHTML = `${artist} ${message}`;
    }
    request.send();
}