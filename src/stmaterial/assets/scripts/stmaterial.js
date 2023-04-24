import Gumshoe from "./gumshoe-patched.js";

var tocScroll = null;
var header = null;
var lastScrollTop = window.pageYOffset || document.documentElement.scrollTop;
const GO_TO_TOP_OFFSET = 64;

function scrollHandlerForHeader() {
  if (Math.floor(header.getBoundingClientRect().top) == 0) {
    header.classList.add("scrolled");
  } else {
    header.classList.remove("scrolled");
  }
}

function scrollHandlerForBackToTop(positionY) {
  if (positionY < GO_TO_TOP_OFFSET) {
    document.documentElement.classList.remove("show-back-to-top");
  } else {
    if (positionY < lastScrollTop) {
      document.documentElement.classList.add("show-back-to-top");
    } else if (positionY > lastScrollTop) {
      document.documentElement.classList.remove("show-back-to-top");
    }
  }
  lastScrollTop = positionY;
}

function scrollHandlerForTOC(positionY) {
  if (tocScroll === null) {
    return;
  }

  // top of page.
  if (positionY == 0) {
    tocScroll.scrollTo(0, 0);
  } else if (
    // bottom of page.
    Math.ceil(positionY) >=
    Math.floor(document.documentElement.scrollHeight - window.innerHeight)
  ) {
    tocScroll.scrollTo(0, tocScroll.scrollHeight);
  } else {
    // somewhere in the middle.
    const current = document.querySelector(".scroll-current");
    if (current == null) {
      return;
    }

    // https://github.com/pypa/pip/issues/9159 This breaks scroll behaviours.
    // // scroll the currently "active" heading in toc, into view.
    // const rect = current.getBoundingClientRect();
    // if (0 > rect.top) {
    //   current.scrollIntoView(true); // the argument is "alignTop"
    // } else if (rect.bottom > window.innerHeight) {
    //   current.scrollIntoView(false);
    // }
  }
}

function scrollHandler(positionY) {
  scrollHandlerForHeader();
  scrollHandlerForBackToTop(positionY);
  scrollHandlerForTOC(positionY);
}

////////////////////////////////////////////////////////////////////////////////
// Setup
////////////////////////////////////////////////////////////////////////////////
function setupScrollHandler() {
  // Taken from https://developer.mozilla.org/en-US/docs/Web/API/Document/scroll_event
  let last_known_scroll_position = 0;
  let ticking = false;

  window.addEventListener("scroll", function (e) {
    last_known_scroll_position = window.scrollY;

    if (!ticking) {
      window.requestAnimationFrame(function () {
        scrollHandler(last_known_scroll_position);
        ticking = false;
      });

      ticking = true;
    }
  });
  window.scroll();
}

function addTOCInteractivity() {
  document.addEventListener('gumshoeActivate', function (event) {
    const navLinks = document.querySelectorAll(".table-of-contents li>a");

    navLinks.forEach((navLink) => {
      navLink.parentElement.classList.remove("active");
    });

    const activeNavLinks = document.querySelectorAll(".table-of-contents li.scroll-current>a");
    activeNavLinks.forEach((navLink) => {
      navLink.parentElement.classList.add("active");
    });
  });
}

function setupScrollSpy() {
  if (tocScroll === null) {
    return;
  }

  // Scrollspy -- highlight table on contents, based on scroll
  new Gumshoe(".table-of-contents a", {
    reflow: true,
    recursive: true,
    navClass: "scroll-current",
    nested: true,
    nestedClass: 'scroll-current', // 
    events: true,
    offset: () => {
      let rem = parseFloat(getComputedStyle(document.documentElement).fontSize);
      return header.getBoundingClientRect().height + 0.5 * rem + 1;
    },
  });
}

function setup() {
  setupScrollHandler();
  addTOCInteractivity();
  setupScrollSpy();
}

function init_materialize() {
  // Detect touch screen and enable scrollbar if necessary
  function is_touch_device() {
    try {
      document.createEvent('TouchEvent');
      return true;
    } catch (e) {
      return false;
    }
  }

  // Mobile Overflow
  if (is_touch_device()) {
    document.querySelector('#nav-mobile').style.overflow = 'auto';
  }

  // Theme
  const theme = localStorage.getItem('theme');
  const themeSwitch = document.querySelector('#theme-switch');
  const setTheme = (isDark) => {
    if (isDark) {
      themeSwitch.classList.add('is-dark');
      themeSwitch.querySelector('i').innerText = 'light_mode';
      themeSwitch.title = 'Switch to light mode';
    }
    else {
      themeSwitch.classList.remove('is-dark');
      themeSwitch.querySelector('i').innerText = 'dark_mode';
      themeSwitch.title = 'Switch to dark mode';
    }
  }
  if (themeSwitch) {
    // Load
    if (theme) setTheme(true);
    // Change
    themeSwitch.addEventListener('click', e => {
      e.preventDefault();
      if (!themeSwitch.classList.contains('is-dark')) {
        // Dark Theme
        document.documentElement.setAttribute('theme', 'dark');
        localStorage.setItem('theme', 'dark');
        setTheme(true);
      }
      else {
        // Light Theme
        document.documentElement.removeAttribute('theme');
        localStorage.removeItem('theme');
        setTheme(false);
      }
    });
  }


  M.Sidenav.init(document.querySelectorAll('.stm-sidenav'), {});
  M.Dropdown.init(document.querySelectorAll('.dropdown-trigger'), { constrainWidth: false, });

}


////////////////////////////////////////////////////////////////////////////////
// Main entrypoint
////////////////////////////////////////////////////////////////////////////////
function main() {
  document.body.parentNode.classList.remove("no-js");
  init_materialize();
  header = document.querySelector("header");
  tocScroll = document.querySelector(".toc-scroll");
  setup();
}

document.addEventListener("DOMContentLoaded", main);
