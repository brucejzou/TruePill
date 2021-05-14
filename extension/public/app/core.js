/* eslint-disable eqeqeq */
/* eslint-disable no-undef */
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
var height = 60;
var observer = new MutationObserver(function(mutations) {
  var posts = document.querySelectorAll('[data-pagelet^="FeedUnit_"]');
  if (posts.length == 0) {
    console.log("big booty bitches");
    var overall = document.querySelectorAll('[class="k4urcfbm"]');
    while (overall.length < 3) {
      window.setTimeout(null,50);
      overall = document.querySelectorAll('[class="k4urcfbm"]');
    }
    posts = overall[f.length - 1].childNodes;
  }
  console.log(posts)
  posts.forEach(post => {
    var menu = post.querySelector('[aria-haspopup="menu"]');
    console.log(menu);
    if (menu == null || menu.parentElement == null || menu.parentElement.parentElement.querySelector('[class="true_img"]') == null ) {
      var elem = document.createElement("img");
      elem.src = chrome.extension.getURL("assets/True Pill - UI Icon Small.png");
      elem.style.paddingTop = "12px";
      elem.style.maxWidth = "4%";
      elem.style.maxHeight = "4%";
      elem.setAttribute("class", "true_img");
      menu.parentElement.parentElement.appendChild(elem);
      elem.addEventListener("click", function(e) {
        getBias('http://localhost:5000/api/truepill/', post, 0)
        .then(data => {
          console.log("Request complete! response:", data);
          if (data.bias !== undefined) {
            //alert("The bias of this article is " + data.bias);
            console.log(data.article_url);
            var div = document.createElement("div");
            div.id = (data.article_url)
            div.style.width = "360px";
            div.style.alignItems = "center";
            div.style.height = height + "px";
            div.style.background = "rgba(256, 256, 256, 1)";
            div.style.padding = "15px";
            div.style.borderRadius = "25px";
            div.style.boxShadow = "2px 2px 10px rgba(0, 0, 0, 0.2)";
            div.style.textAlign = "center";
            div.style.position = "absolute";
            var rect = elem.getBoundingClientRect();
            div.style.left = rect.left + window.scrollX - 180 + 'px';
            div.style.top = rect.top + window.scrollY + 30 + 'px';
            div.style.z = 100;
            // var left = document.createElement("div");
            // var right = document.createElement("div");
            // left.style.backgroundColor = "yellow";
            // left.style.width = "12%";
            // right.style.backgroundColor = "blue";
            // right.style.width = "50%";
            var bias = document.createElement("p");
            //var bar = document.createElement("img");
            //bar.src = chrome.extension.getURL("assets/bar.png");
            // var scale = document.createElement("img");
            // scale.src = chrome.extension.getURL("assets/scale.png");
            // scale.style.maxWidth = "100%";
            // scale.style.maxHeight = "100%";
            // left.appendChild(scale);
            var fontcolor = "gray";
            if (data.bias == "LEFT" || data.bias == "LEFT_CENTER") {
              fontcolor = "blue";
            }
            if (data.bias == "RIGHT" || data.bias == "RIGHT_CENTER") {
              fontcolor = "red";
            }
            if (data.bias == "CENTER") {
              fontcolor = "purple";
            }
            // var header = document.createElement("div");
            // header.style.flexDirection = "row";
            // header.style.justifyContent = "flex-start";
            // header.style.alignItems = "center";
            // header.style.backgroundColor = "red";
            // header.appendChild(left);
            bias.innerHTML = "<b>Bias:</b> " + data.bias.fontcolor(fontcolor).replace("_", " ");
            // right.appendChild(bias);
            //right.appendChild(bar);
            // header.appendChild(right);
            div.appendChild(bias);
            var loader = document.createElement("div");
            var divider = document.createElement("hr");
            loader.id = data.article_url + "_loader"
            loader.style.width = "30px";
            loader.style.alignSelf = "center"
            var loader_wheel = document.createElement("div");
            loader_wheel.style.border = "2px solid rgba(30, 30, 30, 0.5)";
            loader_wheel.style.borderLeft = "4px solid #000";
            loader_wheel.style.borderRadius = "50%";
            loader_wheel.style.height = "20px";
            loader_wheel.style.marginBottom = "10px";
            loader_wheel.style.width = "20px";
            
            loader.appendChild(loader_wheel);
            div.appendChild(divider);
            div.appendChild(loader);
            document.body.appendChild(div);
            document.getElementById(data.article_url + "_loader").animate([
              { transform: 'rotate(0deg)' },
              { transform: 'rotate(360deg)' }
            ], {
              duration: 1000,
              iterations: Infinity
            }
            
            );
            getBias('http://localhost:5000/api/truepill/', post, 1)
            .then(data => {
              
              if (data.suggested_articles !== undefined) {
                // var articles = document.createElement("img");
                // articles.style.maxWidth = "30%";
                // articles.style.maxHeight = "30%";
                var rem_load = document.getElementById(data.article_url + "_loader");
                rem_load.remove();
                div = document.getElementById(data.article_url)
                div.style.height = height + 20 + 60 * data.suggested_articles.length + "px";
                var suggested = document.createElement("div");
                // var divider = document.createElement("hr");
                // suggested.appendChild(articles);
                suggested.innerHTML += "<p><b>Related Articles: </b> Similar articles from various news sources.</p>";
                for (var i = 0; i < data.suggested_articles.length; i++) {
                  var article = document.createElement("div");
                  fontcolor = "gray";
                  if (data.suggested_articles[i].bias == "LEFT" || data.suggested_articles[i].bias == "LEFT_CENTER") {
                    fontcolor = "blue";
                  }
                  if (data.suggested_articles[i].bias == "RIGHT" || data.suggested_articles[i].bias == "RIGHT_CENTER") {
                    fontcolor = "red";
                  }
                  if (data.suggested_articles[i].bias == "CENTER") {
                    fontcolor = "purple";
                  }
                  article.innerHTML += "<p><a href =\"" + data.suggested_articles[i].article_url + "\"><b>" + getDomain(data.suggested_articles[i].article_url).toUpperCase() + "</b></a></p>";
                  article.innerHTML += "<p>Bias rating: " +  data.suggested_articles[i].bias.fontcolor(fontcolor).replace("_", " ") + "</p>";
                  suggested.appendChild(article);
                }
                // div.appendChild(divider);
                div.appendChild(suggested);
              }
              document.body.appendChild(div);
              overlays.push(div);
            });
          }
        });
      }, false);
      //elem.onclick = function() { getBias('http://localhost:5000/api/truepill/', post); }
    }
  });
});

function addObserverIfDesiredNodeAvailable() {
  var feed = document.querySelector('[role="feed"]');
  if (!feed){
    f = document.querySelectorAll('[class="k4urcfbm"]');
    feed = f[f.length - 1];
    if(f.length < 3) {
      console.log("timeout");
      window.setTimeout(addObserverIfDesiredNodeAvailable,50);
      return;
    }
  }
  console.log("found feed", feed);
  var config = { attributes: true, childList: true, characterData: true };
  observer.observe(feed, config);
}

addObserverIfDesiredNodeAvailable();

function getBias(serv_url, post, num_sugg) {
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
  let data = {article_url: fb_url,
  number_suggestions: num_sugg};

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

function getDomain(url) {
    var match = url.match(/:\/\/(www[0-9]?\.)?(.[^/:]+)/i);
    if (match != null && match.length > 2 && typeof match[2] === 'string' && match[2].length > 0) {
      var parts = match[2].split('.').reverse();
      if (parts != null && parts.length > 1) {
          domain = parts[1];
          return domain;
      }
    }
    return null;
}

// NEED TO ADD CREDIT TO APP PAGE LATER
// credit for scale
//<div>Icons made by <a href="" title="Kiranshastry">Kiranshastry</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
// credit for Articles
//<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
