import json

from flask import url_for
from app.env import db

from typing import List

from sqlalchemy import Integer, String, ForeignKey, Table, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property


from sqlalchemy.sql.expression import Select


# class Organism(db.Model):
#     __tablename__ = "bib_organismes"
#     __table_args__ = {"schema": "utilisateurs"}
#     id_organisme: Mapped[int] = mapped_column(Integer, primary_key=True)
#     nom_organisme: Mapped[str] = mapped_column(String, unique=True, nullable=False)

cor_siecles_monu_lieu = Table(
    "cor_siecles_monu_lieu",
    db.metadata,
    db.Column("siecle_monu_lieu_id", ForeignKey("bib_siecle.id_siecle")),
    db.Column("monument_lieu_id", ForeignKey("t_monuments_lieux.id_monument_lieu")),
)


cor_natures_monu_lieu = Table(
    "cor_natures_monu_lieu",
    db.metadata,
    db.Column(
        "monu_lieu_nature_id", ForeignKey("bib_monu_lieu_natures.id_monu_lieu_nature")
    ),
    db.Column("monument_lieu_id", ForeignKey("t_monuments_lieux.id_monument_lieu")),
)

cor_etat_cons_monu_lieu = Table(
    "cor_etat_cons_monu_lieu",
    db.metadata,
    db.Column(
        "etat_cons_monu_lieu_id",
        ForeignKey("bib_etats_conservation.id_etat_conservation"),
    ),
    db.Column("monument_lieu_id", ForeignKey("t_monuments_lieux.id_monument_lieu")),
)

cor_source_auteur_monu_lieu = Table(
    "cor_source_auteur_monu_lieu",
    db.metadata,
    db.Column(
        "source_auteur_monu_lieu_id",
        ForeignKey("bib_source_auteur.id_source_auteur"),
    ),
    db.Column("monument_lieu_id", ForeignKey("t_monuments_lieux.id_monument_lieu")),
)

cor_contributeurs_monu_lieu = Table(
    "cor_contributeurs_monu_lieu",
    db.metadata,
    db.Column(
        "contributeur_monu_lieu_id",
        ForeignKey("bib_contributeur.id_contributeur"),
    ),
    db.Column("monument_lieu_id", ForeignKey("t_monuments_lieux.id_monument_lieu")),
)

cor_redacteurs_monu_lieu = Table(
    "cor_redacteurs_monu_lieu",
    db.metadata,
    db.Column(
        "redacteur_monu_lieu_id",
        ForeignKey("bib_redacteur.id_redacteur"),
    ),
    db.Column("monument_lieu_id", ForeignKey("t_monuments_lieux.id_monument_lieu")),
)

cor_materiaux_monu_lieu = Table(
    "cor_materiaux_monu_lieu",
    db.metadata,
    db.Column(
        "materiau_monu_lieu_id",
        ForeignKey("bib_materiaux.id_materiau"),
    ),
    db.Column("monument_lieu_id", ForeignKey("t_monuments_lieux.id_monument_lieu")),
)

cor_medias_mob_img = Table(
    "cor_medias_mob_img",
    db.metadata,
    db.Column(
        "media_mob_img_id",
        ForeignKey("t_medias.id_media"),
    ),
    db.Column("mobilier_image_id", ForeignKey("t_mobiliers_images.id_mobilier_image")),
)


cor_medias_monu_lieu = Table(
    "cor_medias_monu_lieu",
    db.metadata,
    db.Column(
        "media_monu_lieu_id",
        ForeignKey("t_medias.id_media"),
    ),
    db.Column("monument_lieu_id", ForeignKey("t_monuments_lieux.id_monument_lieu")),
)

cor_medias_pers_mo = Table(
    "cor_medias_pers_mo",
    db.metadata,
    db.Column(
        "media_pers_mo_id",
        ForeignKey("t_medias.id_media"),
    ),
    db.Column("pers_morale_id", ForeignKey("t_pers_morales.id_pers_morale")),
)

cor_medias_pers_phy = Table(
    "cor_medias_pers_phy",
    db.metadata,
    db.Column(
        "media_pers_phy_id",
        ForeignKey("t_medias.id_media"),
    ),
    db.Column("pers_physique_id", ForeignKey("t_pers_physiques.id_pers_physique")),
)


class Media(db.Model):
    __tablename__ = "t_medias"
    id: Mapped[int] = mapped_column("id_media", primary_key=True)
    titre: Mapped[str] = mapped_column("titre_media")
    chemin: Mapped[str] = mapped_column("chemin_media", JSON)
    commentaires: Mapped[str] = mapped_column()
    media_auteur: Mapped[str] = mapped_column()
    source: Mapped[str] = mapped_column()

    @hybrid_property
    def url(self):
        try:
            media_path_list = json.loads(self.chemin)
            path = "/".join(media_path_list[0]["path"].split("/")[2:])
        except:
            return ""

        return url_for("main.media", filename=path, _external=True)


class BibMateriaux(db.Model):
    __tablename__ = "bib_materiaux"
    id_materiau: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column("materiau_type")


class BibContributeur(db.Model):
    __tablename__ = "bib_contributeur"
    id_contributeur: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column("contributeur_nom")


class BibSiecle(db.Model):
    __tablename__ = "bib_siecle"
    id_siecle: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column("siecle_list")


class BibMonuLieuNature(db.Model):
    __tablename__ = "bib_monu_lieu_natures"
    id_monu_lieu_nature: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column("monu_lieu_nature_type")


class BibEtatConservation(db.Model):
    __tablename__ = "bib_etats_conservation"
    id_etat_conservation: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column("etat_conservation_type")


class BibSourceAuteur(db.Model):
    __tablename__ = "bib_source_auteur"
    id_source_auteur: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column("source_auteur")


class BibRedacteur(db.Model):
    __tablename__ = "bib_redacteur"
    id_redacteur: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column("redacteur_nom")


class MobilierImage(db.Model):
    __tablename__ = "t_mobiliers_images"

    id: Mapped[int] = mapped_column("id_mobilier_image", primary_key=True)
    title: Mapped[str] = mapped_column("titre_mob_img")
    description: Mapped[str] = mapped_column()
    histoire: Mapped[str] = mapped_column("historique")
    source: Mapped[str] = mapped_column("source")
    bibliographie: Mapped[str] = mapped_column()
    date_creation: Mapped[str] = mapped_column()
    date_maj: Mapped[str] = mapped_column()
    publie: Mapped[bool] = mapped_column()

    medias: Mapped[List[Media]] = relationship(secondary=cor_medias_mob_img)


class PersonneMorale(db.Model):
    __tablename__ = "t_pers_morales"

    id: Mapped[int] = mapped_column("id_pers_morale", primary_key=True)
    title: Mapped[str] = mapped_column("titre_pers_mo")
    source: Mapped[str] = mapped_column("sources")
    bibliographie: Mapped[str] = mapped_column()
    date_creation: Mapped[str] = mapped_column()
    date_maj: Mapped[str] = mapped_column()
    publie: Mapped[bool] = mapped_column()
    medias: Mapped[List[Media]] = relationship(secondary=cor_medias_pers_mo)


class PersonnePhysique(db.Model):
    __tablename__ = "t_pers_physiques"

    id: Mapped[int] = mapped_column("id_pers_physique", primary_key=True)
    prenom_nom_pers_phy: Mapped[str] = mapped_column()
    source: Mapped[str] = mapped_column("sources")
    date_creation: Mapped[str] = mapped_column()
    date_maj: Mapped[str] = mapped_column()
    publie: Mapped[bool] = mapped_column()

    medias: Mapped[List[Media]] = relationship(secondary=cor_medias_pers_phy)


class MonumentLieu(db.Model):
    __tablename__ = "t_monuments_lieux"

    id: Mapped[int] = mapped_column("id_monument_lieu", primary_key=True)
    title: Mapped[str] = mapped_column("titre_monu_lieu")
    description: Mapped[str] = mapped_column()
    histoire: Mapped[str] = mapped_column()
    protection: Mapped[str] = mapped_column()
    sources: Mapped[str] = mapped_column("source")
    bibliographie: Mapped[str] = mapped_column()
    date_creation: Mapped[str] = mapped_column()
    date_maj: Mapped[str] = mapped_column()
    publie: Mapped[bool] = mapped_column()

    siecles: Mapped[List[BibSiecle]] = relationship(secondary=cor_siecles_monu_lieu)
    natures: Mapped[List[BibMonuLieuNature]] = relationship(
        secondary=cor_natures_monu_lieu
    )
    etat_conservation: Mapped[List[BibEtatConservation]] = relationship(
        secondary=cor_etat_cons_monu_lieu
    )
    auteurs: Mapped[List[BibSourceAuteur]] = relationship(
        secondary=cor_source_auteur_monu_lieu
    )
    contributeurs: Mapped[List[BibContributeur]] = relationship(
        secondary=cor_contributeurs_monu_lieu
    )

    redacteurs: Mapped[List[BibRedacteur]] = relationship(
        secondary=cor_redacteurs_monu_lieu
    )

    materiaux: Mapped[List[BibMateriaux]] = relationship(
        secondary=cor_materiaux_monu_lieu
    )

    medias: Mapped[List[Media]] = relationship(secondary=cor_medias_monu_lieu)
