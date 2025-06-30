var dato1 = 15;
var dato2 = 9;
var dato3 = 20;

document.write('<h1>Los números ingresados son: ' + dato1 + ', ' + dato2 + ' y ' + dato3 + '</h1>');

if (dato1 === dato2 && dato2 === dato3) {
    document.write('<h1>Los tres números son iguales: ' + dato1 + '</h1>');
} else if (dato1 >= dato2 && dato1 >= dato3) {
    if (dato1 === dato2 || dato1 === dato3) {
        document.write('<h1>Hay un empate. El mayor es: ' + dato1 + '</h1>');
    } else {
        document.write('<h1>El mayor es: ' + dato1 + '</h1>');
    }
} else if (dato2 >= dato1 && dato2 >= dato3) {
    if (dato2 === dato1 || dato2 === dato3) {
        document.write('<h1>Hay un empate. El mayor es: ' + dato2 + '</h1>');
    } else {
        document.write('<h1>El mayor es: ' + dato2 + '</h1>');
    }
} else {
    if (dato3 === dato1 || dato3 === dato2) {
        document.write('<h1>Hay un empate. El mayor es: ' + dato3 + '</h1>');
    } else {
        document.write('<h1>El mayor es: ' + dato3 + '</h1>');
    }
}