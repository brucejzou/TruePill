document.addEventListener('mousemove', function (e) {
  var srcElement = e.srcElement;
  // Lets check if our underlying element is a DIV.
  while (srcElement != null && srcElement.getAttribute("data-pagelet") != 'FeedUnit_1') {
    if (srcElement.nodeName == 'A') {
      var url = srcElement.getAttribute("href");
      if (url != null) {
        alert(url);
        console.log(url);
        let data = {article_url : url};
        fetch('http://localhost:5000/api/truepill/', {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          //mode: 'no-cors',
          method: "POST",
          body: JSON.stringify(data)
        }).then(res => {
          console.log("Request complete! response:", res);
        });
      }
    }
    srcElement = srcElement.parentNode;
    //console.log(srcElement);
  }
  console.log(srcElement)
}, false);
