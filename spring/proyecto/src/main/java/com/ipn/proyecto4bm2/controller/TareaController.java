package com.ipn.proyecto4bm2.controller;

import com.ipn.proyecto4bm2.domain.Tarea;
import com.ipn.proyecto4bm2.services.TareaService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@CrossOrigin(origins = {"*"})
@RequestMapping("/api")
public class TareaController {
    
    @Autowired
    private TareaService tareaService;

    // Obtener todas las tareas
    @GetMapping("/tareas")
    @ResponseStatus(HttpStatus.OK)
    public List<Tarea> getAllTareas(){
        return tareaService.findAll();
    }

    // Obtener una tarea por ID
    @GetMapping("/tareas/{id}")
    public ResponseEntity<Tarea> getTareaById(@PathVariable Long id) {
        Tarea tarea = tareaService.findById(id);
        if (tarea != null) {
            return ResponseEntity.ok(tarea);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    // Crear una nueva tarea
    @PostMapping("/tareas")
    public ResponseEntity<Tarea> createTarea(@RequestBody Tarea tarea) {
        Tarea nuevaTarea = tareaService.save(tarea);
        return ResponseEntity.status(HttpStatus.CREATED).body(nuevaTarea);
    }

    // Actualizar una tarea
    @PutMapping("/tareas/{id}")
    public ResponseEntity<Tarea> updateTarea(@PathVariable Long id, @RequestBody Tarea tarea) {
        Tarea tareaExistente = tareaService.findById(id);
        if (tareaExistente != null) {
            tarea.setIdTarea(id);
            Tarea tareaActualizada = tareaService.update(tarea);
            return ResponseEntity.ok(tareaActualizada);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    // Eliminar una tarea
    @DeleteMapping("/tareas/{id}")
    public ResponseEntity<Void> deleteTarea(@PathVariable Long id) {
        Tarea tarea = tareaService.findById(id);
        if (tarea != null) {
            tareaService.deleteById(id);
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    // Marcar tarea como completada
    @PatchMapping("/tareas/{id}/completar")
    public ResponseEntity<Tarea> completarTarea(@PathVariable Long id) {
        Tarea tarea = tareaService.findById(id);
        if (tarea != null) {
            tarea.setCompletada(true);
            Tarea tareaActualizada = tareaService.update(tarea);
            return ResponseEntity.ok(tareaActualizada);
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}
