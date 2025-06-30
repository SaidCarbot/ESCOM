package com.ipn.proyecto4bm2.services;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.ipn.proyecto4bm2.domain.Tarea;
import com.ipn.proyecto4bm2.domain.TareaRepository;

@Service
public class TareaServiceImpl implements TareaService {

    @Autowired
    private TareaRepository tareaRepository;

    @Override
    public List<Tarea> findAll() {
        return tareaRepository.findAll();
    }

    @Override
    public Tarea findById(Long id) {
        return tareaRepository.findById(id).orElse(null);
    }

    @Override
    public Tarea save(Tarea tarea) {
        return tareaRepository.save(tarea);
    }

    @Override
    public void deleteById(Long id) {
        tareaRepository.deleteById(id);
    }

    @Override
    public Tarea update(Tarea tarea) {
        return tareaRepository.save(tarea);
    }
}
