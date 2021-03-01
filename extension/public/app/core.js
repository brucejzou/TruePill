// var current_url;
// var overlays = [];
//
// document.addEventListener('mousemove', function (e) {
//   if(typeof movewait != 'undefined'){
//     clearTimeout(movewait);
//   }
//   movewait = setTimeout(function(){
//     var srcElement = e.srcElement;
//     while (srcElement != null && srcElement.getAttribute("data-pagelet") != 'FeedUnit_1') {
//       //var rect = srcElement.getBoundingClientRect();
//       if (srcElement.nodeName == 'A') {
//         var url = srcElement.getAttribute("href");
//         if (current_url == url) {
//           return;
//         }
//         if (overlays.length != 0) {
//           document.body.removeChild(overlays[0]);
//           overlays.pop();
//         }
//         current_url = url;
//         if (url != null && url.substring(0,25).valueOf() != "https://www.facebook.com/".valueOf()) {
//           let data = {article_url : url};
//           getBias('http://localhost:5000/api/truepill/', data)
//           .then(data => {
//             //console.log("Request complete! response:", data);
//             if (data.bias !== undefined) {
//               var div = document.createElement("div");
//               div.style.width = "80px";
//               div.style.height = "80px";
//               div.style.background = "rgba(256, 256, 256, 0.7)";
//               div.style.padding = "40px";
//               div.style.textAlign = "center";
//               div.innerHTML = "The bias of this article is " + data.bias;
//               div.style.position = "absolute";
//               div.style.left = e.pageX+'px';
//               div.style.top = e.pageY+'px';
//               div.style.z = 100;
//               document.body.appendChild(div);
//               overlays.push(div);
//             }
//           });
//           break;
//         }
//       }
//       srcElement = srcElement.parentNode;
//     }
//   },200);
// }, false);
//
// function getBias(url, data) {
//   return fetch(url, {
//     headers: {
//       'Accept': 'application/json',
//       'Content-Type': 'application/json'
//     },
//     method: "POST",
//     body: JSON.stringify(data)
//   }).then(res => res.json());
// }



var overlays = [];
var feed = document.querySelector('[role="feed"]');

var observer = new MutationObserver(function(mutations) {
  var posts = document.querySelectorAll('[data-pagelet^="FeedUnit_"]');
  console.log(posts)
  posts.forEach(post => {
    var menu = post.querySelector('[aria-haspopup="menu"]');
    if ( menu.parentElement.parentElement.querySelector('[class="true_img"]') == null ) {
      var elem = document.createElement("img");
      elem.src = chrome.extension.getURL("assets/True Pill - UI Icon.png");
      elem.style.paddingTop = "12px";
      elem.setAttribute("class", "true_img");
      menu.parentElement.parentElement.appendChild(elem);
      elem.addEventListener("click", function(e) {
        getBias('http://localhost:5000/api/truepill/', post)
        .then(data => {
          console.log("Request complete! response:", data);
          if (data.bias !== undefined) {
            alert("The bias of this article is " + data.bias);
            console.log(data.article_url);
            var div = document.createElement("div");
            div.style.width = "130px";
            div.style.height = "80px";
            div.style.background = "rgba(256, 256, 256, 1)";
            div.style.padding = "15px";
            div.style.borderRadius = "25px";
            div.style.boxShadow = "2px 2px 10px rgba(0, 0, 0, 0.2)";
            div.style.textAlign = "center";
            div.style.position = "absolute";
            var rect = elem.getBoundingClientRect();
            div.style.left = rect.left + window.scrollX - 65 + 'px';
            div.style.top = rect.top + window.scrollY + 30 + 'px';
            div.style.z = 100;
            var bias = document.createElement("div");
            var suggested = document.createElement("div");
            var divider = document.createElement("hr");
            bias.innerHTML = "The bias of this article is " + data.bias;
            suggested.innerHTML = "Here are some suggested articles...";
            div.appendChild(bias);
            div.appendChild(divider);
            div.appendChild(suggested);
            document.body.appendChild(div);
            overlays.push(div);
          }
        });
      }, false);
      //elem.onclick = function() { getBias('http://localhost:5000/api/truepill/', post); }
    }
  });
});

var config = { attributes: true, childList: true, characterData: true };
observer.observe(feed, config);

function getBias(serv_url, post) {
  var fb_url = null;
  Array.from(post.querySelectorAll('A')).every(link => {
    fb_url = link.getAttribute("href");
    if (fb_url != null && fb_url.substring(0, 4).valueOf() == "http".valueOf() && fb_url.substring(0, 25).valueOf() != "https://www.facebook.com/".valueOf()) {
      return false;
    };
    fb_url = null;
    return true;
  });
  if ( fb_url == null ) {
    alert("No article detected.")
    return false
  };
  let data = {article_url: fb_url};
  return fetch(serv_url, {
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    //mode: 'no-cors',
    method: "POST",
    body: JSON.stringify(data)
  }).then(res => res.json());
}
