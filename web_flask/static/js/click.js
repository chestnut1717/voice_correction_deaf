// function httpGet(theUrl)
// {
//     var xmlhr = new XMLHttpRequest();
//     xmlhr.open( "POST", theUrl, false);
//     xmlhr.send( null );
//     document.getElementById('get').innerHTML=xmlhr.responseText;
//     // console.log(xmlhr.responseText);
//     return xmlhr.responseText;
// }

// // var button_click = document.getElementsByClassName('lev_button');
// // url = '/record'
// // button_click.addEventListener('click', httpGet(url), false);
document.getElementById("myButton").onclick = function () {
    location.href = "www.yoursite.com";
};
