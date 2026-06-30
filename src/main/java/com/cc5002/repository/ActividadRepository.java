package com.cc5002.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import com.cc5002.model.Actividad;

public interface ActividadRepository extends JpaRepository<Actividad, Integer> {
    // query para buscar q en el nombre, descripcion o nombre comuna
    @Query("""
        SELECT a FROM Actividad a
        WHERE LOWER(a.nombre) LIKE LOWER(CONCAT('%', :q, '%'))
           OR LOWER(a.descripcion) LIKE LOWER(CONCAT('%', :q, '%'))
           OR LOWER(a.miembro.comuna.nombre) LIKE LOWER(CONCAT('%', :q, '%'))
        """)
    List<Actividad> buscar(@Param("q") String q);
}