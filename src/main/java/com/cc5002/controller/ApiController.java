package com.cc5002.controller;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import com.cc5002.model.Actividad;
import com.cc5002.service.ActividadService;

@Controller
public class ApiController {

    @Autowired
    private ActividadService service;

    @GetMapping("/buscador")
    public String buscador() {
        return "buscador";
    }

    @GetMapping("/api/buscar")
    @ResponseBody
    public ResponseEntity<?> buscar(@RequestParam String q) {
        if (q == null || q.trim().length() < 3) {
            return ResponseEntity.badRequest().body("Mínimo 3 caracteres");
        }
        // busqueda
        List<Actividad> actividades = service.buscar(q.trim());
    

        List<Map<String, Object>> resultado = new ArrayList<>();

        // map de ORM a dict
        for (Actividad a : actividades) {
            Map<String, Object> map = new HashMap<>();
            map.put("id", a.getId());
            map.put("nombre", a.getNombre());
            map.put("descripcion", a.getDescripcion());
            map.put("dia", a.getDia());
            map.put("tipo", a.getTipo());
            map.put("comuna", a.getMiembro().getComuna().getNombre());
            map.put("miembro", a.getMiembro().getNombre());
            map.put("promedio", service.getPromedio(a.getId()));
            resultado.add(map);
        }

        return ResponseEntity.ok(resultado);
    }

    @PostMapping("/api/nota")
    @ResponseBody
    public ResponseEntity<?> agregarNota(@RequestBody Map<String, Integer> body) {
        Integer actividadId = body.get("actividadId");
        Integer valor = body.get("valor");

        try {
            Map<String, Object> result = service.agregarNota(actividadId, valor);
            return ResponseEntity.ok(result);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
}