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

// function getBias(url, data) {
//   return fetch(url, {
//     headers: {
//       'Accept': 'application/json',
//       'Content-Type': 'application/json'
//     },
//     //mode: 'no-cors',
//     method: "POST",
//     body: JSON.stringify(data)
//   }).then(res => res.json());
// }

var feed = document.querySelectorAll('[data-pagelet^="FeedUnit_"]');
console.log(feed)
feed.forEach(post => {
  var elem = document.createElement("img");
  elem.src = chrome.extension.getURL("logo-small.png")
  post.querySelector('[aria-haspopup="menu"]').parentElement.parentElement.appendChild(elem); 
  console.log(post);
});