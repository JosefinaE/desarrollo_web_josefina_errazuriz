package com.cc5002.model;

import jakarta.persistence.*;

@Entity
@Table(name = "nota", schema = "tarea2")
public class Nota {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "actividad_id", nullable = false)
    private Integer actividadId;

    @Column(name = "nota", nullable = false)
    private Integer nota;

    public Nota() {}

    public Nota(Integer actividadId, Integer nota) {
        this.actividadId = actividadId;
        this.nota = nota;
    }

    public Integer getId() { return id; }
    public Integer getActividadId() { return actividadId; }
    public Integer getNota() { return nota; }
}