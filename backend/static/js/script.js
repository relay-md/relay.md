document.addEventListener('DOMContentLoaded', () => {

  /* Burger Menu
  ***************************************************************/
  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

  // Add a click event on each of them
  $navbarBurgers.forEach( el => {
    el.addEventListener('click', () => {

      // Get the target from the "data-target" attribute
      const target = el.dataset.target;
      const $target = document.getElementById(target);

      // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      el.classList.toggle('is-active');
      $target.classList.toggle('is-active');

    });
  });

  /* Light/dark switcher
  ***************************************************************/
  var DARK = "dark";
  var LIGHT = "light";
  var mode = "light";
  var LOCAL_STORAGE_KEY = "relaymd-dark"
  try {
    store = localStorage
  } catch (err) {
    // Do nothing. The user probably blocks cookies.
  }
  function loadCss() {
    // fix css loading via vite
    // https://github.com/vitejs/vite/issues/8976
    const css = document.createElement('style')
    css.innerHTML = `
/* Prevent inconsistencies for positioning */
.nightowl-light body{
filter: invert(0%);
}

.nightowl-dark {
/* Firefox fallback. */
background-color: #111;
}

.nightowl-dark body {
filter: invert(100%) hue-rotate(180deg);
}

/* Do not invert media (revert the invert). */
.nightowl-dark img:not(.brand-logo),
.nightowl-dark video,
.nightowl-dark iframe,
.nightowl-dark .nightowl-daylight
{
filter: invert(100%) hue-rotate(180deg);
}

/* Improve contrast on icons. */
.nightowl-dark .icon {
filter: invert(15%) hue-rotate(180deg);
}

/* Re-enable code block backgrounds. */
.nightowl-dark pre {
filter: invert(6%);
}

/* Improve contrast on list item markers. */
.nightowl-dark li::marker {
color: #666;
}
`
    document.head.appendChild(css)
  }

  window.addEventListener('load', () => {
    loadCss()
    checkForRememberedValue()
    updateMode()
    initializeSwitcher()
  })

  function enableDarkMode() {
    mode = DARK
    const htmlElement = document.querySelector('html')
    if (htmlElement) {
      htmlElement.classList.remove('nightowl-light')
      htmlElement.classList.add('nightowl-dark')
    }
  }

  function enableLightMode() {
    mode = LIGHT
    const htmlElement = document.querySelector('html')
    if (htmlElement) {
      htmlElement.classList.remove('nightowl-dark')
      htmlElement.classList.add('nightowl-light')
    }
  }

  function toggleMode() {
    mode = mode === DARK ? LIGHT : DARK
    updateMode()
  }

  function updateMode() {
    if (mode === DARK) {
      enableDarkMode()
    } else {
      enableLightMode()
    }
    setSwitcherIcon()
  }

  function setSwitcherIcon() {
    const switcher = document.getElementById('switcher-default')
    if (switcher) {
      const lightIcon =
        '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="width: 25px; height:25px;">\n' +
          '  <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />\n' +
          '</svg>'
      const darkIcon =
        '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="width: 25px; height:25px;">\n' +
          '  <path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" />\n' +
          '</svg>'
      switcher.innerHTML = mode === LIGHT ? darkIcon : lightIcon
    }
  }

  function initializeSwitcher() {
    const switcher = document.getElementById('switcher-default');
    switcher.style.width = '24px'
    switcher.style.height = '24px'
    switcher.style.cursor = 'pointer'
    switcher.style.transition = 'all 0.3s ease-in-out'
    switcher.style.overflow = 'hidden'
    switcher.style.color = 'black'

    switcher.addEventListener('click', () => {
      toggleMode()
      storeModeInLocalStorage()
    })
    setSwitcherIcon()
  }
  function storeModeInLocalStorage() {
    if (mode !== null) {
      try {
        if (store) {
          store.setItem(LOCAL_STORAGE_KEY, mode)
        }
      } catch (err) {
        // Do nothing. The user probably blocks cookies.
      }
    }
  }
  function checkForRememberedValue() {
    let rememberedValue = null
    try {
      if (store) {
        rememberedValue = store.getItem(LOCAL_STORAGE_KEY)
      }
    } catch (err) {
      // Do nothing. The user probably blocks cookies.
    }
    if (rememberedValue && [DARK, LIGHT].includes(rememberedValue)) {
      mode = rememberedValue
    } else if (hasNativeDarkPrefersColorScheme()) {
      mode = DARK
    }
  }
  function hasNativeDarkPrefersColorScheme() {
    return (
      window.matchMedia &&
        (window.matchMedia('(prefers-color-scheme: dark)').matches ||
          window.matchMedia('(prefers-color-scheme:dark)').matches)
    )
  }

});




/* Get documents per api
***************************************************************/
async function get_document(id) {
  let base_url = "https://api.relay.md/v1/doc/";
  // For development purpose only:
  // base_url = "http://localhost:5001/v1/doc/";
  const response = await fetch(base_url + id, {
    method: "GET",
    headers: {
      "Content-Type": "text/markdown",
      "X-API-Key": "{{access_token}}"
    }
  });
  if (!response.ok) {
    throw new Error(response.statusText);
  }

  if (response.headers.get("content-type") == "application/json") {
    res = await response.json();
    throw Error(res.error.message);
  }
  return await response.text();
}

/* Postprocess markdown to something nicer to read
***************************************************************/
function post_process_markdown(doc) {
  var FRONTMATTER_EXPR = /---\n(.*)?\n---/s
  var body = doc.replace(FRONTMATTER_EXPR, "");
  var frontmatter = doc.match(FRONTMATTER_EXPR);
  var metadata = jsyaml.load(frontmatter[1]);
  showdown.extension('codehighlight', function() {
    function htmlunencode(text) {
      return (
        text
        .replace(/&amp;/g, '&')
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
      );
    }
    return [
      {
        type: 'output',
        filter: function (text, converter, options) {
          // use new shodown's regexp engine to conditionally parse codeblocks
          var left  = '<pre><code\\b[^>]*>',
          right = '</code></pre>',
          flags = 'g',
          replacement = function (wholematch, match, left, right) {
            // unescape match to prevent double escaping
            match = htmlunencode(match);
            return '<pre class="hljs"><code>' + hljs.highlightAuto(match).value + right;
          };
          return showdown.helper.replaceRecursiveRegExp(text, replacement, left, right, flags);
        }
      }
    ];
  });
  var converter = new showdown.Converter({
    "extensions": ["codehighlight"]
  });
  return [converter.makeHtml(body), metadata];
}
