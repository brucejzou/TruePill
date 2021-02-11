# Getting Started with the Extension

### `yarn install`

### `yarn build`

You should run `run build` inside the `extension` folder.

Then, go to your [Chrome Extensions settings](chrome://extensions/), click `Load unpacked` and selected the newly created `build` folder inside of `extension`. The extension should be added to your Google Chrome.

# Using the Extension

You can go to Facebook and mouse over the posts on your Feed. Posts with links from news sources should trigger a pop-up displaying the medias bias rating of the site. Due to the way we've implemented it right now, multiple pop-ups will occur (it's an issue with using a mouse_move event, which was a temporary placeholder) and it's best to close the tab and reopen Facebook.
