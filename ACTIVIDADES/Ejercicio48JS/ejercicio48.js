// --------- Parte 1: Números pares del 1 al 100 ---------
document.write('<h2>Números pares del 1 al 100:</h2>');
for (var i = 1; i <= 100; i++) {
    if (i % 2 === 0) {
        document.write(i + '   ');
    }
}

// --------- Parte 2: Suma de los primeros 100 números ---------
var suma = 0;
for (var j = 1; j <= 100; j++) {
    suma += j;
}

document.write('<h2>Suma de los primeros 100 números:</h2>');
document.write('<p>' + suma + '</p>');
