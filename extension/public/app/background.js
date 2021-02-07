function getName(name) {
    // All this api does is echo back the name
    const url = 'https://do2ewch6z8.execute-api.us-east-2.amazonaws.com/default/hello-world-python';
    let data = {
        name: name
    }
    let fetchData = {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    }
    console.log(fetchData)
    fetch(url, fetchData)
        .then(
            function(response) {
                if (response.status !== 200) {
                    console.log('There was a problem connecting to the API. Status Code: ' + response.status);
                    return;
                }

                response.json().then(function(data) {
                    console.log("data.name: " + data.name);
                    alert("Welcome to " + data.name);
                    return;
                  }
                );
            }
        )
        .catch(function(err) {
            console.log('Fetch error :-S', err);
        });
}

(function() {
  const tabStorage = {};
  const networkFilters = {
      urls: [
          "https://www.facebook.com/*"
      ]
  };

  chrome.webRequest.onBeforeRequest.addListener((details) => {
      const { tabId, requestId } = details;
      if (!tabStorage.hasOwnProperty(tabId)) {
          return;
      }

      tabStorage[tabId].requests[requestId] = {
          requestId: requestId,
          url: details.url,
          startTime: details.timeStamp,
          status: 'pending'
      };
      console.log(tabStorage[tabId].requests[requestId]);
  }, networkFilters);

  chrome.webRequest.onCompleted.addListener((details) => {
      const { tabId, requestId } = details;

      if (!tabStorage.hasOwnProperty(tabId) || !tabStorage[tabId].requests.hasOwnProperty(requestId)) {
          return;
      }

      const request = tabStorage[tabId].requests[requestId];
      var re = new RegExp("https://www.facebook.com/$")
      console.log(details.url)
      if (re.test(details.url)) {
          getName("True Pill");
          chrome.windows.create({
            'url': chrome.extension.getURL("app/popup.html"),
            'height': 200,
            'width': 200,
            'type': "popup",
            'focused': true
          });
      }

      Object.assign(request, {
          endTime: details.timeStamp,
          requestDuration: details.timeStamp - request.startTime,
          status: 'complete'
      });
      console.log(tabStorage[tabId].requests[details.requestId]);
  }, networkFilters);

  chrome.webRequest.onErrorOccurred.addListener((details)=> {
      const { tabId, requestId } = details;
      if (!tabStorage.hasOwnProperty(tabId) || !tabStorage[tabId].requests.hasOwnProperty(requestId)) {
          return;
      }

      const request = tabStorage[tabId].requests[requestId];
      Object.assign(request, {
          endTime: details.timeStamp,
          status: 'error',
      });
      console.log(tabStorage[tabId].requests[requestId]);
  }, networkFilters);

  chrome.tabs.onActivated.addListener((tab) => {
      const tabId = tab ? tab.tabId : chrome.tabs.TAB_ID_NONE;
      if (!tabStorage.hasOwnProperty(tabId)) {
          tabStorage[tabId] = {
              id: tabId,
              requests: {},
              registerTime: new Date().getTime()
          };
      }
  });
  chrome.tabs.onRemoved.addListener((tab) => {
      const tabId = tab.tabId;
      if (!tabStorage.hasOwnProperty(tabId)) {
          return;
      }
      tabStorage[tabId] = null;
  });

  chrome.runtime.onMessage.addListener((msg, sender, response) => {
    switch (msg.type) {
        case 'popupInit':
            response(tabStorage[msg.tabId]);
            break;
        default:
            response('unknown request');
            break;
    }
   });
}());
