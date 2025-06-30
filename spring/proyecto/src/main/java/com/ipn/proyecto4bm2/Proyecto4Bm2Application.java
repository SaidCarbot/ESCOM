package com.ipn.proyecto4bm2;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import com.ipn.proyecto4bm2.domain.Tarea;
import com.ipn.proyecto4bm2.domain.TareaRepository;

@SpringBootApplication
public class Proyecto4Bm2Application implements CommandLineRunner{
    @Autowired
    private TareaRepository dao;

    public static void main(String[] args) {
        SpringApplication.run(Proyecto4Bm2Application.class, args);
    }

    @Override
    public void run(String... args) throws Exception {
        // Crear nueva tarea
        Tarea t = new Tarea();
        t.setNombreTarea("Me deben muchas actividades");
        t.setDescripcionTarea("Aun no las publico en plataforma y espero que cuando ya esten vayan corriendo y las suban");
        
        System.out.println("=== TAREA ANTES DE GUARDAR ===");
        System.out.println(t);
        
        // Guardar en la base de datos
        Tarea tareaGuardada = dao.save(t);
        
        System.out.println("\n=== TAREA GUARDADA EN LA BASE DE DATOS ===");
        System.out.println("ID generado: " + tareaGuardada.getIdTarea());
        System.out.println("Nombre: " + tareaGuardada.getNombreTarea());
        System.out.println("Descripción: " + tareaGuardada.getDescripcionTarea());
        System.out.println("Completada: " + tareaGuardada.getCompletada());
        
        // Mostrar todas las tareas de la base de datos
        System.out.println("\n=== TODAS LAS TAREAS EN LA BASE DE DATOS ===");
        var todasLasTareas = dao.findAll();
        
        if (todasLasTareas.isEmpty()) {
            System.out.println("No hay tareas en la base de datos.");
        } else {
            System.out.println("Total de tareas: " + todasLasTareas.size());
            int contador = 1;
            for (Tarea tarea : todasLasTareas) {
                System.out.println("\n--- Tarea " + contador + " ---");
                System.out.println("ID: " + tarea.getIdTarea());
                System.out.println("Nombre: " + tarea.getNombreTarea());
                System.out.println("Descripción: " + tarea.getDescripcionTarea());
                System.out.println("Completada: " + tarea.getCompletada());
                contador++;
            }
        }
        
        System.out.println("\n=== FIN DE LA DEMOSTRACIÓN ===");
    }
}
