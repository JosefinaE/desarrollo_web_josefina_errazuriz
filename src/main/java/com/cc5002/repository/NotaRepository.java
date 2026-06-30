package com.cc5002.repository;

import com.cc5002.model.Nota;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface NotaRepository extends JpaRepository<Nota, Integer> {
    List<Nota> findByActividadId(Integer actividadId);
}