function setHeight() {
    var div = document.getElementsByClassName('card-wrapper');
    for (let i = 0; i < div.length; i++) {
        computedStyle = getComputedStyle(div[i]);
        width = parseFloat(computedStyle.width);
        rootFontSize = parseFloat(getComputedStyle(document.documentElement).fontSize);
        widthRem = width / rootFontSize;
        heightRem = (widthRem * 9) / 16; /* 16:9 aspect ratio */
        div[i].style.height = heightRem + 'rem';
    }
}
setHeight();

window.addEventListener('resize', setHeight);