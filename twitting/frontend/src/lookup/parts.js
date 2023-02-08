function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function delivered(method, endpoint, callback, data){
    let jsonData;
    if(data){
        jsonData= JSON.stringify(data)
    }
    const xhr= new XMLHttpRequest()
    const url= `http://localhost:8000/api${endpoint}`
    xhr.responseType= "json"
    const csrftoken= getCookie('csrftoken');
    xhr.open(method, url)
    xhr.setRequestHeader("Content-Type", "application/json")
    if(csrftoken){
        xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
    }
    xhr.onload= function(){
        if(xhr.status=== 403){
            const detail= xhr.response.detail
            if(detail=== "Authentication credentials were not provided."){
                if(window.location.href.indexOf("login")=== -1){
                  window.location.href= "login/?showLoginRequired=true"
                }
            }
        }
        callback(xhr.response, xhr.status)
    }
    xhr.onerror= function(e){
        callback({"message":"The request was an error"}, 400)
    }
    xhr.send(jsonData)
}

export function createTweet(newTweet, callback){
    delivered("POST", "/twe/create", callback, {content:newTweet})
}

export function tweet_feed(callback, nextUrl){
    let endpoint= "/twe/feed/"
    if(nextUrl!== null && nextUrl!== undefined){
        endpoint= nextUrl.replace("http://localhost:8000/api", "")
    }
    delivered("GET", endpoint, callback)
}
export function existing_tweet(username, callback, nextUrl){
     let endpoint= "/twe"
     if(username){
         endpoint=`/twe/?username=${username}`
     }
     if(nextUrl!== null && nextUrl!== undefined){
         endpoint= nextUrl.replace("http://localhost:8000/api", "")
     }
     delivered("GET", endpoint, callback)
}

export function tweetAction(id, action, callback){
    const data={id: id, action:action}
    delivered("POST", "/twe/action", callback, data)
}

export function profileDetail(username, callback){
    delivered("GET", `/profiles/${username}/`, callback)
}

export function profileFollowToggle(username, action, callback){
    const data={action: `${action && action}`.toLowerCase()}
    delivered("POST", `/profiles/${username}/follow`, callback, data)
}


export function tweetDetail(id, callback){
    delivered("GET", `/twe/${id}/`, callback)
}


