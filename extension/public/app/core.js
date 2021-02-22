// document.addEventListener('mousemove', function (e) {
//   var srcElement = e.srcElement;
//   // Lets check if our underlying element is a DIV.
//   while (srcElement != null && srcElement.getAttribute("data-pagelet") != 'FeedUnit_1') {
//     if (srcElement.nodeName == 'A') {
//       var url = srcElement.getAttribute("href");
//       if (url != null && url.substring(0,25).valueOf() != "https://www.facebook.com/".valueOf())  {
//         //alert(url);
//         //console.log(url);
//         console.log(url.substring(0,25));
//         let data = {article_url : url};
//         getBias('http://localhost:5000/api/truepill/', data)
//         .then(data => {
//           console.log("Request complete! response:", data);
//           if (data.bias !== undefined) {
//             alert("The bias of this article is " + data.bias);
//             console.log(data.article_url);
//           }
//         });
//         break;
//       }
//     }
//     srcElement = srcElement.parentNode;
//     //console.log(srcElement);
//   }
// }, false);



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
      elem.onclick = function() { getBias('http://localhost:5000/api/truepill/', post); }
 
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
  }).then(res => res.json()).then(data => {
    console.log("Request complete! response:", data);
    if (data.bias !== undefined) {
      alert("The bias of this article is " + data.bias);
      console.log(data.article_url);
    }
  });
}