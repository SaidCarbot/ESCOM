const contenedor = document.getElementById("contenedor");

function agregarCard(titulo, instruccion, contenidoHTML) {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
        <h2>${titulo}</h2>
        <div class="instruccion">${instruccion}</div>
        <div class="result">${contenidoHTML}</div>
    `;
    contenedor.appendChild(card);
}

// ---------- Ejercicio 1 ----------
let inst1 = "Leer un número y mostrar si dicho número es o no es par.";
let num1 = parseInt(prompt("Ejercicio 1:\nLeer un número y mostrar si dicho número es o no es par.\n\nIngresa un número:"));
let res1 = (num1 % 2 === 0) ? `El número ${num1} es par.` : `El número ${num1} no es par.`;
agregarCard("1. Número par o impar", inst1, res1);

// ---------- Ejercicio 2 ----------
let inst2 = "Leer un número y mostrar su tabla de multiplicar del 1 al 10.";
let num2 = parseInt(prompt("Ejercicio 2:\nLeer un número y mostrar su tabla de multiplicar del 1 al 10.\n\nIngresa el número:"));
let tabla = "";
for (let i = 1; i <= 10; i++) {
    tabla += `${num2} x ${i} = ${num2 * i}<br>`;
}
agregarCard("2. Tabla de multiplicar", inst2, tabla);

// ---------- Ejercicio 3 ----------
let inst3 = "Leer dos números y calcular el producto solo utilizando sumas sucesivas.";
let a = parseInt(prompt("Ejercicio 3: " + inst3 + "\n\nIngresa el primer número:"));
let b = parseInt(prompt("Ejercicio 3: "  + inst3 + "\n\nIngresa el segundo número:"));
let producto = 0;
for (let i = 0; i < Math.abs(b); i++) producto += Math.abs(a);
if ((a < 0 && b > 0) || (a > 0 && b < 0)) producto = -producto;
agregarCard("3. Producto mediante sumas", inst3, `El producto de ${a} y ${b} es: ${producto}`);

// ---------- Ejercicio 4 ----------
let inst4 = "Leer una secuencia de n números, almacenarlos en un arreglo y mostrar la posición del mayor valor leído.";
let n4 = parseInt(prompt("Ejercicio 4: " + inst4 + "\n\n¿Cuántos números vas a ingresar?"));
let arr4 = [], mayor = -Infinity, pos = 0;
for (let i = 0; i < n4; i++) {
    let val = parseInt(prompt(`Ejercicio 4:\n${inst4}\n\nIngresa el número ${i + 1}:`));
    arr4.push(val);
    if (val > mayor) {
        mayor = val;
        pos = i;
    }
}
agregarCard("4. Mayor en arreglo", inst4, `Valores: [${arr4.join(', ')}]<br>Mayor valor: ${mayor} en posición ${pos}`);

// ---------- Ejercicio 5 ----------
let inst5 = "Dado 2 vectores A y B de n elementos cada uno, obtener un arreglo C con A[i] + B[i].";
let n5 = parseInt(prompt("Ejercicio 5: " + inst5 + "\n\n¿Cuántos elementos tendrán los vectores?"));
let A = [], B = [], C = [];
for (let i = 0; i < n5; i++) A.push(parseInt(prompt(`Ejercicio 5:\n${inst5}\n\nVector A - Elemento ${i + 1}:`)));
for (let i = 0; i < n5; i++) B.push(parseInt(prompt(`Ejercicio 5:\n${inst5}\n\nVector B - Elemento ${i + 1}:`)));
for (let i = 0; i < n5; i++) C.push(A[i] + B[i]);
agregarCard("5. Suma de vectores", inst5, `
    A: [${A.join(', ')}]<br>
    B: [${B.join(', ')}]<br>
    C: [${C.join(', ')}]
`);

// ---------- Ejercicio 6 ----------
let inst6 = "Calcular la media de una secuencia de números proporcionada por el usuario.";
let n6 = parseInt(prompt("Ejercicio 6: " + inst6 + "\n\n¿Cuántos números vas a ingresar?"));
let suma6 = 0;
for (let i = 0; i < n6; i++) suma6 += parseFloat(prompt(`Ejercicio 6:\n${inst6}\n\nIngresa el número ${i + 1}:`));
let media = suma6 / n6;
agregarCard("6. Media de números", inst6, `La media es: ${media.toFixed(2)}`);

// ---------- Ejercicio 7 ----------
let inst7 = "Dada una secuencia de números leídos y almacenados en un arreglo [A], mostrar dichos números en orden.";
let n7 = parseInt(prompt("Ejercicio 7: " + inst7 + "\n\n¿Cuántos números vas a ingresar?"));
let arr7 = [];
for (let i = 0; i < n7; i++) arr7.push(parseFloat(prompt(`Ejercicio 7:\n${inst7}\n\nIngresa el número ${i + 1}:`)));
agregarCard("7. Mostrar números en orden", inst7, `[${arr7.join(', ')}]`);

// ---------- Ejercicio 8 ----------
let inst8 = "Dada una secuencia de textos, visualizar: La longitud, en mayúsculas y en minúsculas.";
let n8 = parseInt(prompt("Ejercicio 8: " + inst8 + "\n\n¿Cuántos textos vas a ingresar?"));
let resultado8 = "";
for (let i = 0; i < n8; i++) {
    let txt = prompt(`Ejercicio 8:\n${inst8}\n\nIngresa el texto ${i + 1}:`);
    resultado8 += `
        <p><strong>Texto:</strong> ${txt}</p>
        <p>Longitud: ${txt.length}</p>
        <p>Mayúsculas: ${txt.toUpperCase()}</p>
        <p>Minúsculas: ${txt.toLowerCase()}</p><hr>
    `;
}
agregarCard("8. Análisis de textos", inst8, resultado8);
