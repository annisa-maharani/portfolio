let x, y, z;
x = document.getElementById('content');
y = x.getElementsByTagName('img');
for (z = 0; z < y.length; z++) {
    y[z].className = 'img-fluid';
    y[z].style = null;
}
//
// let a, b, c, d;
// b = x.getElementsByTagName('p');
// a = x.getElementsByTagName('a');
// for (c = 0; c < b.length; c++){
//     b[c].className = 'text-break text-decoration-none';
// }
//
// for (d = 0; d <= a.length; d++){
//     a[d].className = 'text-decoration-none text-primary'
// }
