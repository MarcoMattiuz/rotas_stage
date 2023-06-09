
function setHeight() {
    var div = document.getElementsByClassName('card-wrapper');
    for (let i = 0; i < div.length; i++) {
        computedStyle = getComputedStyle(div[i]);
        width = parseFloat(computedStyle.width);
        rootFontSize = parseFloat(getComputedStyle(document.documentElement).fontSize);
        widthRem = width / rootFontSize; // Larghezza convertita in rem
        heightRem = (widthRem * 9) / 16; /* 16:9 aspect ratio */
        div[i].style.height = heightRem + 'rem';
    }
}

// Chiamata iniziale per impostare l'altezza iniziale
setHeight();

// Chiamata di setHeight() quando la finestra viene ridimensionata
window.addEventListener('resize', setHeight);