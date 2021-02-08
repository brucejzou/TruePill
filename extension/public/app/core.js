// Unique ID for the className.
var MOUSE_VISITED_CLASSNAME = 'crx_mouse_visited';

// Previous dom, that we want to track, so we can remove the previous styling.
var prevDOM = null;

// Mouse listener for any move event on the current document.
document.addEventListener('mousemove', function (e) {
  var srcElement = e.srcElement;
  // Lets check if our underlying element is a DIV.
  while (srcElement != null && srcElement.getAttribute("data-pagelet") != 'FeedUnit_1') {
    if (srcElement.nodeName == 'A') {
      var url = srcElement.getAttribute("href");
      alert(url);
    }
    srcElement = srcElement.parentNode;
    console.log(srcElement);
  }
  console.log(srcElement)
}, false);