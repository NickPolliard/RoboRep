(switchOn) => {
    document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');
    return window.dash_clientside.no_update
}