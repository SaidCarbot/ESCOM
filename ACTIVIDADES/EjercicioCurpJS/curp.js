document.getElementById("curpForm").addEventListener("submit", function(event) {
      event.preventDefault();

      const nombre = document.getElementById("nombre").value.toUpperCase().trim();
      const paterno = document.getElementById("paterno").value.toUpperCase().trim();
      const materno = document.getElementById("materno").value.toUpperCase().trim();
      const fecha = document.getElementById("fecha").value.trim();
      const sexo = document.getElementById("sexo").value.trim();
      const estado = document.getElementById("estado").value.trim();

      const vocales = "AEIOU";

      function primeraVocalInterna(txt) {
        for (let i = 1; i < txt.length; i++) {
          if (vocales.includes(txt[i])) return txt[i];
        }
        return 'X';
      }

      function primeraConsonanteInterna(txt) {
        for (let i = 1; i < txt.length; i++) {
          if (!vocales.includes(txt[i]) && txt[i] !== 'Ñ') return txt[i];
        }
        return 'X';
      }

      const letra1 = paterno[0] || 'X';
      const vocal1 = primeraVocalInterna(paterno);
      const letra2 = materno[0] || 'X';
      const letra3 = nombre[0] || 'X';

      const [anio, mes, dia] = fecha.split("-");
      const fechaCURP = anio.slice(2) + mes + dia;

      const cons1 = primeraConsonanteInterna(paterno);
      const cons2 = primeraConsonanteInterna(materno);
      const cons3 = primeraConsonanteInterna(nombre);

      const homoclave = "00"; // fija para simplificar

      const curp = `${letra1}${vocal1}${letra2}${letra3}${fechaCURP}${sexo}${estado}${cons1}${cons2}${cons3}${homoclave}`;

      const salida = document.getElementById("resultado");
      salida.innerHTML = `<strong>CURP generado:</strong><br>${curp}`;
      salida.style.display = "block";
    });