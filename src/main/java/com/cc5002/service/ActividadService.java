package com.cc5002.service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.cc5002.model.Actividad;
import com.cc5002.model.Nota;
import com.cc5002.repository.ActividadRepository;
import com.cc5002.repository.NotaRepository;

@Service
public class ActividadService {

    @Autowired private ActividadRepository actividadRepo;
    @Autowired private NotaRepository notaRepo;

    public List<Actividad> buscar(String q) {
        return actividadRepo.buscar(q);
    }

    public Double getPromedio(Integer actividadId) {
        // obtener notas y promediarlas
    List<Nota> notas = notaRepo.findByActividadId(actividadId);
        if (notas.isEmpty()) return null;
        return notas.stream().mapToInt(Nota::getNota).average().orElse(0);
    }


    public Map<String, Object> agregarNota(Integer actividadId, Integer valor) {
        if (valor == null || valor < 1 || valor > 7) {
            throw new IllegalArgumentException("Nota debe ser entre 1 y 7");
        }

        notaRepo.save(new Nota(actividadId, valor));

        List<Nota> notas = notaRepo.findByActividadId(actividadId);
        double promedio = notas.stream().mapToInt(Nota::getNota).average().orElse(0);

        Map<String, Object> result = new HashMap<>();
        result.put("promedio", promedio);
        result.put("cantidad", notas.size());
        return result;
    }
}