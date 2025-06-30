package com.ipn.proyecto4bm2.services;

import com.ipn.proyecto4bm2.domain.Tarea;
import java.util.List;

public interface TareaService {
    public List<Tarea> findAll();
    public Tarea findById(Long id);
    public Tarea save(Tarea tarea);
    public void deleteById(Long id);
    public Tarea update(Tarea tarea);
}
