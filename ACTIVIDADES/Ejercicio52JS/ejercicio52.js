// --------- Parte 1: Números pares del 1 al 100 usando while ---------
document.write('<h2>Números pares del 1 al 100 (while):</h2>');

var i = 1;
while (i <= 100) {
    if (i % 2 === 0) {
        document.write(i + '   ');
    }
    i++;
}

// --------- Parte 2: Suma de los primeros 100 números usando while ---------
var j = 1;
var suma = 0;

while (j <= 100) {
    suma += j;
    j++;
}

document.write('<h2>Suma de los primeros 100 números (while):</h2>');
document.write('<p>' + suma + '</p>');
