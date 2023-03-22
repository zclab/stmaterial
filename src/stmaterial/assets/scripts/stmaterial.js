import "./materialize.js";

document.addEventListener("DOMContentLoaded", function () {
    document.body.parentNode.classList.remove("no-js");

    // Detect touch screen and enable scrollbar if necessary
    function is_touch_device() {
        try {
            document.createEvent('TouchEvent');
            return true;
        } catch (e) {
            return false;
        }
    }


    // Floating-Fixed Table of Contents
    const tocWrapperHeight = 260; // Max height of ads.
    const socialHeight = 95; // Height of unloaded social media in footer.
    const tocElem = document.querySelector('.toc-wrapper .table-of-contents');
    const tocHeight = tocElem ? tocElem.getBoundingClientRect().height : 0;

    const footerElem = document.querySelector('body > footer');
    const footerOffset = footerElem ? (
        // https://youmightnotneedjquery.com/#offset
        footerElem.getBoundingClientRect().top - window.scrollY + document.documentElement.clientTop
    ) : 0;
    const bottomOffset = footerOffset - socialHeight - tocHeight - tocWrapperHeight;

    const nav = document.querySelector('nav');
    const indexBanner = document.querySelector('#index-banner');
    const tocWrappers = document.querySelectorAll('.toc-wrapper');

    if (nav)
        M.Pushpin.init(tocWrappers, { top: nav.getBoundingClientRect().height, bottom: bottomOffset });
    else if (indexBanner)
        M.Pushpin.init(tocWrappers, { top: indexBanner.getBoundingClientRect().height, bottom: bottomOffset });
    else
        M.Pushpin.init(tocWrappers, { top: 0, bottom: bottomOffset });


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

    M.ScrollSpy.init(document.querySelectorAll('.scrollspy'), {});
    M.Sidenav.init(document.querySelectorAll('.sidenav'), {});

    M.FloatingActionButton.init(document.querySelectorAll('.fixed-action-btn'), {});
    M.FloatingActionButton.init(document.querySelectorAll('.fixed-action-btn.horizontal'), {
        direction: 'left'
    });
    M.FloatingActionButton.init(document.querySelectorAll('.fixed-action-btn.click-to-toggle'), {
        direction: 'left',
        hoverEnabled: false
    });
    M.FloatingActionButton.init(document.querySelectorAll('.fixed-action-btn.toolbar'), {
        toolbarEnabled: true
    });

});