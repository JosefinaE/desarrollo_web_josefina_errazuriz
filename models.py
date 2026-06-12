from datetime import datetime
from typing import List, Optional

from sqlalchemy import TIMESTAMP, DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

DIAS = ("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo")
TIPOS = ("arte", "deporte", "tecnología", "social", "recreación", "otra")

TIPO_MIEMBRO = ("estudiante_pre", "estudiante_post", "funcionario", "academico")
DEPTOS = (
    "DCC",
    "DIM",
    "DFI",
    "DIE",
    "DII",
    "Geologia",
    "Astronomia",
    "Ing. en Minas",
    "Ing. Mecanica",
    "Ing. Civil",
)


class Base(DeclarativeBase):
    pass


class Region(Base):
    __tablename__ = "region"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    comunas: Mapped[List["Comuna"]] = relationship(back_populates="region")


class Comuna(Base):
    __tablename__ = "comuna"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    region_id: Mapped[int] = mapped_column(ForeignKey("region.id"), nullable=False)

    region: Mapped["Region"] = relationship(back_populates="comunas")
    miembros: Mapped[List["Miembro"]] = relationship(back_populates="comuna")


class Miembro(Base):
    __tablename__ = "miembro"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(80), nullable=False)
    telefono: Mapped[str] = mapped_column(String(15), nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    comuna_id: Mapped[int] = mapped_column(ForeignKey("comuna.id"), nullable=False)
    tipo: Mapped[str] = mapped_column(Enum(*TIPO_MIEMBRO), nullable=False)
    departamento: Mapped[str] = mapped_column(Enum(*DEPTOS), nullable=True)

    comuna: Mapped["Comuna"] = relationship(back_populates="miembros")
    actividades: Mapped[List["Actividad"]] = relationship(back_populates="miembro")


class Actividad(Base):
    __tablename__ = "actividad"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False)

    dia: Mapped[str] = mapped_column(Enum(*DIAS), nullable=False)
    hora_inicio: Mapped[str] = mapped_column(String(5), nullable=False)
    duracion: Mapped[str] = mapped_column(String(5), nullable=False)
    tipo: Mapped[str] = mapped_column(Enum(*TIPOS), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    miembro_id: Mapped[int] = mapped_column(ForeignKey("miembro.id"), nullable=False)

    miembro: Mapped["Miembro"] = relationship(back_populates="actividades")
    fotos: Mapped[List["Foto"]] = relationship(
        back_populates="actividad", cascade="all, delete-orphan"
    )
    comentarios: Mapped[List["Comentario"]] = relationship(
        back_populates="actividad", cascade="all, delete-orphan"
    )


class Foto(Base):
    __tablename__ = "foto"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ruta_archivo: Mapped[str] = mapped_column(String(300), nullable=False)
    nombre_archivo: Mapped[str] = mapped_column(String(300), nullable=False)
    actividad_id: Mapped[int] = mapped_column(
        ForeignKey("actividad.id"), nullable=False
    )

    actividad: Mapped["Actividad"] = relationship(back_populates="fotos")


class Comentario(Base):
    __tablename__ = "comentario"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    texto: Mapped[str] = mapped_column(String(300), nullable=False)
    fecha: Mapped[object] = mapped_column(
        TIMESTAMP, nullable=False, default=datetime.utcnow
    )

    actividad_id: Mapped[int] = mapped_column(
        ForeignKey("actividad.id", ondelete="NO ACTION", onupdate="NO ACTION"),
        nullable=False,
    )

    actividad: Mapped["Actividad"] = relationship(back_populates="comentarios")
