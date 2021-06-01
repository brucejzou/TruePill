console.log("Extension running");
var height = 80;
var observer = new MutationObserver(function(mutations) {
  var posts = Array.from(document.querySelector('[aria-label="Timeline: Your Home Timeline"]').children[0].children);
  console.log(posts)
  posts.forEach(post => {
    var menu = post.querySelector('[aria-haspopup="menu"]');
    console.log(menu);
    if (menu == null || menu.parentElement == null || menu.parentElement.parentElement.querySelector('[class="true_img"]') == null ) {
      var elem = document.createElement("img");
      elem.src = chrome.extension.getURL("assets/True Pill - UI Icon Small.png");
      elem.style.paddingTop = "2px";
      elem.style.maxWidth = "55%";
      elem.style.maxHeight = "55%";
      elem.setAttribute("class", "true_img");
      menu.parentElement.parentElement.appendChild(elem);
      elem.addEventListener("click", function(e) {
        e.stopPropagation();
        getBias('http://localhost:5000/api/truepill/', post, 0)
        .then(data => {
          console.log("Request complete! response:", data);
          if (document.getElementById(data.article_url) != null) {
            document.getElementById(data.article_url).remove();
          }
          else if (data.bias !== undefined) {
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

            var header = document.createElement("div");
            header.style.display = "flex";
            header.style.flexDirection = "row";
            header.style.justifyContent = "flex-start";
            header.style.alignItems = "flex-start";

            var headerleft = document.createElement("div");
            var headerright = document.createElement("div");
            headerleft.style.width = "12%";
            headerleft.style.marginTop = "10px";

            headerright.style.width = "80%";
            headerright.style.marginLeft = "10px";
            headerright.style.textAlign = "left";
            headerright.style.lineHeight = "30%";

            var scale = document.createElement("img");
            scale.src = chrome.extension.getURL("assets/scale.png");
            scale.style.maxWidth = "100%";
            scale.style.maxHeight = "100%";
            headerleft.appendChild(scale);
            header.appendChild(headerleft);

            var fontcolor = "gray";
            var marginunit = 0;
            if (data.bias == "LEFT") {
              fontcolor = "blue";
            }
            if (data.bias == "LEFT_CENTER") {
              fontcolor = "blue";
              marginunit = 63;
            }
            if (data.bias == "RIGHT") {
              fontcolor = "red";
              marginunit = 253;
            }
            if (data.bias == "RIGHT_CENTER") {
              fontcolor = "red";
              marginunit = 189;
            }
            if (data.bias == "CENTER") {
              fontcolor = "purple";
              marginunit = 126;
            }
            var bias = document.createElement("div");
            bias.style.textAlign = "left";
            bias.innerHTML += "<p style=\"font-size:20px\"><b>Bias Rating: </b>"+ data.bias.fontcolor(fontcolor).replace("_", " ") + "</p>";
            headerright.appendChild(bias);
            var bar = document.createElement("img");
            bar.src = chrome.extension.getURL("assets/bar.png");
            headerright.appendChild(bar);
            var pointer = document.createElement("img");
            pointer.src = chrome.extension.getURL("assets/pointer.png");
            pointer.style.marginLeft = marginunit + "px";
            pointer.style.height = "10px";
            pointer.style.width = "10px";
            headerright.appendChild(pointer);
            header.appendChild(headerright);
            div.appendChild(header);

            var loader = document.createElement("div");
            loader.id = data.article_url + "_loader"
            loader.style.width = "30px";
            loader.style.alignSelf = "center";
            loader.style.justifyContent = "center";
            loader.style.margin = "20px"
            loader.style.marginLeft = "145px";

            var loader_wheel = document.createElement("div");
            loader_wheel.style.border = "2px solid rgba(30, 30, 30, 0.5)";
            loader_wheel.style.borderLeft = "4px solid #000";
            loader_wheel.style.borderRadius = "50%";
            loader_wheel.style.height = "20px";
            loader_wheel.style.marginBottom = "10px";
            loader_wheel.style.width = "20px";

            loader.appendChild(loader_wheel);
            div.style.height = height + 60 + "px";
            var divider = document.createElement("hr");
            div.appendChild(divider);
            div.appendChild(loader);
            document.body.appendChild(div);

            var footer = document.createElement("div");
            footer.style.display = "flex";
            footer.style.flexDirection = "row";
            footer.style.justifyContent = "flex-start";
            footer.style.alignItems = "flex-start";

            var footerleft = document.createElement("div");
            var footerright = document.createElement("div");
            footerleft.style.width = "12%";
            footerleft.style.marginTop = "10px";

            footerright.style.width = "80%";
            footerright.style.marginLeft = "10px";
            footerright.style.textAlign = "left";
            footerright.style.lineHeight = "30%";

            document.getElementById(data.article_url + "_loader").animate([
              { transform: 'rotate(0deg)' },
              { transform: 'rotate(360deg)' }
            ], {
              duration: 1000,
              iterations: Infinity
            });

            getBias('http://localhost:5000/api/truepill/', post, 1)
            .then(data => {
              if (data.suggested_articles !== undefined) {
                div.style.height = height + 60 + 72 * data.suggested_articles.length + "px";
                var rem_load = document.getElementById(data.article_url + "_loader");
                rem_load.remove();
                var div_load = document.getElementById(data.article_url);
                div_load.remove();

                var articles = document.createElement("img");
                articles.src = chrome.extension.getURL("assets/application.png");
                articles.style.maxWidth = "100%";
                articles.style.maxHeight = "100%";
                footerleft.appendChild(articles);
                footer.appendChild(footerleft);

                footerright.innerHTML += "<p style=\"font-size:20px\"><b>Related Articles </b></p>";
                footerright.innerHTML += "<p>Similar articles from various news sources.".fontcolor("gray")+"</p><br><br>";
                if (data.suggested_articles.length == 0) {
                  div.style.height = height + 85 + "px";
                  var article = document.createElement("div");
                  article.style.lineHeight = "100%";
                  fontcolor = "gray";
                  article.innerHTML += "<p>"+ "No related articles could be found".fontcolor("gray") + "</p>";
                  footerright.appendChild(article);
                }
                for (var i = 0; i < data.suggested_articles.length; i++) {
                  var article = document.createElement("div");
                  article.style.lineHeight = "100%";
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
                  article.innerHTML += "<p><a href =\"" + data.suggested_articles[i].article_url + "\"><b>" + getDomain(data.suggested_articles[i].article_url).toUpperCase() + ": </b>" + data.suggested_articles[i].article_title + "</a></p>";
                  article.innerHTML += "<p>"+ "Bias rating: ".fontcolor("gray") +  data.suggested_articles[i].bias.fontcolor(fontcolor).replace("_", " ") + "</p>";
                  footerright.appendChild(article);
                }
                footer.appendChild(footerright);
                div.appendChild(footer);
              }
              document.body.appendChild(div);
          })
        }
      });
      }, false);
      //elem.onclick = function() { getBias('http://localhost:5000/api/truepill/', post); }
    }
  });
});

function addObserverIfDesiredNodeAvailable() {
  console.log("finding Feed");
  var feed = document.querySelector('[aria-label="Timeline: Your Home Timeline"]');
  if(!feed){
    setTimeout(addObserverIfDesiredNodeAvailable,1000);
  } else {
    console.log("found feed", feed);
    var config = { attributes: true, childList: true, characterData: true };
    observer.observe(feed.children[0], config);
  }
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
//<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
