package com.cc5002.model;

import jakarta.persistence.*;

@Entity
@Table(name = "actividad", schema = "tarea2")
public class Actividad {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne
    @JoinColumn(name = "miembro_id", nullable = false)
    private Miembro miembro;

    @Enumerated(EnumType.STRING)
    @Column(name = "dia")
    private Dia dia;

    @Column(name = "hora_inicio")
    private String horaInicio;

    private String duracion;

    @Enumerated(EnumType.STRING)
    @Column(name = "tipo")
    private TipoActividad tipo;

    private String nombre;
    private String descripcion;

    public enum Dia {
        lunes, martes, miércoles, jueves, viernes, sábado, domingo
    }

    public enum TipoActividad {
        arte, deporte, tecnología, social, recreación, otra
    }

    public Integer getId() { return id; }
    public Miembro getMiembro() { return miembro; }
    public Dia getDia() { return dia; }
    public String getHoraInicio() { return horaInicio; }
    public String getDuracion() { return duracion; }
    public TipoActividad getTipo() { return tipo; }
    public String getNombre() { return nombre; }
    public String getDescripcion() { return descripcion; }
}