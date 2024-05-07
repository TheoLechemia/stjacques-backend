import json

from flask import url_for
from app.env import db

from typing import List

from sqlalchemy import Integer, String, ForeignKey, Table, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.expression import Select


from sqlalchemy.orm import raiseload, joinedload

from sqlalchemy import func


cor_siecles_monu_lieu = Table(
    "cor_siecles_monu_lieu",
    db.metadata,
    db.Column("siecle_monu_lieu_id", ForeignKey("bib_siecle.id_siecle")),
    db.Column("monument_lieu_id", ForeignKey("t_monuments_lieux.id_monument_lieu")),
)

cor_siecles_pers_mo = Table(
    "cor_siecles_pers_mo",
    db.metadata,
    db.Column("siecle_pers_mo_id", ForeignKey("bib_siecle.id_siecle")),
    db.Column("pers_morale_id", ForeignKey("t_pers_morales.id_pers_morale")),
)

cor_contributeurs_pers_mo = Table(
    "cor_contributeurs_pers_mo",
    db.metadata,
    db.Column(
        "contributeur_pers_mo_id", ForeignKey("bib_contributeur.id_contributeur")
    ),
    db.Column("pers_morale_id", ForeignKey("t_pers_morales.id_pers_morale")),
)


cor_siecles_pers_phy = Table(
    "cor_siecles_pers_phy",
    db.metadata,
    db.Column("siecle_pers_phy_id", ForeignKey("bib_siecle.id_siecle")),
    db.Column("pers_physique_id", ForeignKey("t_pers_physiques.id_pers_physique")),
)

cor_siecles_mob_img = Table(
    "cor_siecles_mob_img",
    db.metadata,
    db.Column("siecle_mob_img_id", ForeignKey("bib_siecle.id_siecle")),
    db.Column("mobilier_image_id", ForeignKey("t_mobiliers_images.id_mobilier_image")),
)

cor_source_auteur_mob_img = Table(
    "cor_source_auteur_mob_img",
    db.metadata,
    db.Column(
        "source_auteur_mob_img_id", ForeignKey("bib_source_auteur.id_source_auteur")
    ),
    db.Column("mobilier_image_id", ForeignKey("t_mobiliers_images.id_mobilier_image")),
)


cor_materiaux_mob_img = Table(
    "cor_materiaux_mob_img",
    db.metadata,
    db.Column("materiau_mob_img_id", ForeignKey("bib_materiaux.id_materiau")),
    db.Column("mobilier_image_id", ForeignKey("t_mobiliers_images.id_mobilier_image")),
)


cor_contributeurs_mob_img = Table(
    "cor_contributeurs_mob_img",
    db.metadata,
    db.Column(
        "contributeur_mob_img_id", ForeignKey("bib_contributeur.id_contributeur")
    ),
    db.Column("mobilier_image_id", ForeignKey("t_mobiliers_images.id_mobilier_image")),
)

cor_natures_monu_lieu = Table(
    "cor_natures_monu_lieu",
    db.metadata,
    db.Column(
        "monu_lieu_nature_id", ForeignKey("bib_monu_lieu_natures.id_monu_lieu_nature")
    ),
    db.Column("monument_lieu_id", ForeignKey("t_monuments_lieux.id_monument_lieu")),
)

cor_etat_cons_mob_img = Table(
    "cor_etat_cons_mob_img",
    db.metadata,
    db.Column(
        "etat_cons_mob_img_id",
        ForeignKey("bib_etats_conservation.id_etat_conservation"),
    ),
    db.Column("mobilier_image_id", ForeignKey("t_mobiliers_images.id_mobilier_image")),
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


cor_natures_pers_mo = Table(
    "cor_natures_pers_mo",
    db.metadata,
    db.Column(
        "pers_mo_nature_id",
        ForeignKey("bib_pers_mo_natures.id_pers_mo_nature"),
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


cor_modes_deplacements_pers_phy = Table(
    "cor_modes_deplacements_pers_phy",
    db.metadata,
    db.Column(
        "mode_deplacement_id",
        ForeignKey("bib_pers_phy_modes_deplacements.id_mode_deplacement"),
    ),
    db.Column("pers_physique_id", ForeignKey("t_pers_physiques.id_pers_physique")),
)

cor_professions_pers_phy = Table(
    "cor_professions_pers_phy",
    db.metadata,
    db.Column(
        "profession_id",
        ForeignKey("bib_pers_phy_professions.id_profession"),
    ),
    db.Column("pers_physique_id", ForeignKey("t_pers_physiques.id_pers_physique")),
)

cor_periodes_historiques_pers_phy = Table(
    "cor_periodes_historiques_pers_phy",
    db.metadata,
    db.Column(
        "periode_historique_id",
        ForeignKey("bib_pers_phy_periodes_historiques.id_periode_historique"),
    ),
    db.Column("pers_physique_id", ForeignKey("t_pers_physiques.id_pers_physique")),
)


cor_designations_mob_img = Table(
    "cor_designations_mob_img",
    db.metadata,
    db.Column(
        "designation_id",
        ForeignKey("bib_mob_img_designations.id_designation"),
    ),
    db.Column("mobilier_image_id", ForeignKey("t_mobiliers_images.id_mobilier_image")),
)

cor_techniques_mob_img = Table(
    "cor_techniques_mob_img",
    db.metadata,
    db.Column(
        "technique_id",
        ForeignKey("bib_mob_img_techniques.id_technique"),
    ),
    db.Column("mobilier_image_id", ForeignKey("t_mobiliers_images.id_mobilier_image")),
)


cor_monu_lieu_mob_img = Table(
    "cor_monu_lieu_mob_img",
    db.metadata,
    db.Column(
        "monument_lieu_id",
        ForeignKey("t_monuments_lieux.id_monument_lieu"),
    ),
    db.Column("mobilier_image_id", ForeignKey("t_mobiliers_images.id_mobilier_image")),
)

cor_redacteurs_mob_img = Table(
    "cor_redacteurs_mob_img",
    db.metadata,
    db.Column(
        "redacteur_mob_img_id",
        ForeignKey("bib_redacteur.id_redacteur"),
    ),
    db.Column("mobilier_image_id", ForeignKey("t_mobiliers_images.id_mobilier_image")),
)


cor_monu_lieu_pers_mo = Table(
    "cor_monu_lieu_pers_mo",
    db.metadata,
    db.Column(
        "monument_lieu_id",
        ForeignKey("t_monuments_lieux.id_monument_lieu"),
    ),
    db.Column("pers_morale_id", ForeignKey("t_pers_morales.id_pers_morale")),
)


cor_mob_img_pers_mo = Table(
    "cor_mob_img_pers_mo",
    db.metadata,
    db.Column(
        "mobilier_image_id",
        ForeignKey("t_mobiliers_images.id_mobilier_image"),
    ),
    db.Column("pers_morale_id", ForeignKey("t_pers_morales.id_pers_morale")),
)


cor_monu_lieu_pers_phy = Table(
    "cor_monu_lieu_pers_phy",
    db.metadata,
    db.Column(
        "monu_lieu_id",
        ForeignKey("t_monuments_lieux.id_monument_lieu"),
    ),
    db.Column("pers_phy_id", ForeignKey("t_pers_physiques.id_pers_physique")),
)

cor_contributeurs_pers_phy = Table(
    "cor_contributeurs_pers_phy",
    db.metadata,
    db.Column(
        "contributeur_pers_phy_id",
        ForeignKey("bib_contributeur.id_contributeur"),
    ),
    db.Column("pers_physique_id", ForeignKey("t_pers_physiques.id_pers_physique")),
)

cor_redacteurs_pers_phy = Table(
    "cor_redacteurs_pers_phy",
    db.metadata,
    db.Column(
        "redacteur_pers_phy_id",
        ForeignKey("bib_redacteur.id_redacteur"),
    ),
    db.Column("pers_physique_id", ForeignKey("t_pers_physiques.id_pers_physique")),
)


cor_pers_phy_pers_mo = Table(
    "cor_pers_phy_pers_mo",
    db.metadata,
    db.Column(
        "pers_morale_id",
        ForeignKey("t_pers_morales.id_pers_morale"),
    ),
    db.Column("pers_physique_id", ForeignKey("t_pers_physiques.id_pers_physique")),
)

cor_redacteurs_pers_mo = Table(
    "cor_redacteurs_pers_mo",
    db.metadata,
    db.Column(
        "pers_morale_id",
        ForeignKey("t_pers_morales.id_pers_morale"),
    ),
    db.Column("redacteur_pers_mo_id", ForeignKey("bib_redacteur.id_redacteur")),
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
    id: Mapped[int] = mapped_column("id_materiau", primary_key=True)
    name: Mapped[str] = mapped_column("materiau_type")


class BibDesignationMobImg(db.Model):
    __tablename__ = "bib_mob_img_designations"
    id: Mapped[int] = mapped_column("id_designation", primary_key=True)
    name: Mapped[str] = mapped_column("designation_type")


class BibContributeur(db.Model):
    __tablename__ = "bib_contributeur"
    id: Mapped[int] = mapped_column("id_contributeur", primary_key=True)
    name: Mapped[str] = mapped_column("contributeur_nom")


class BibSiecle(db.Model):
    __tablename__ = "bib_siecle"
    id: Mapped[int] = mapped_column("id_siecle", primary_key=True)
    name: Mapped[str] = mapped_column("siecle_list")


class BibMonuLieuNature(db.Model):
    __tablename__ = "bib_monu_lieu_natures"
    id: Mapped[int] = mapped_column("id_monu_lieu_nature", primary_key=True)
    name: Mapped[str] = mapped_column("monu_lieu_nature_type")


class BibEtatConservation(db.Model):
    __tablename__ = "bib_etats_conservation"
    id: Mapped[int] = mapped_column("id_etat_conservation", primary_key=True)
    name: Mapped[str] = mapped_column("etat_conservation_type")


class BibSourceAuteur(db.Model):
    __tablename__ = "bib_source_auteur"
    id: Mapped[int] = mapped_column("id_source_auteur", primary_key=True)
    name: Mapped[str] = mapped_column("source_auteur")


class BibRedacteur(db.Model):
    __tablename__ = "bib_redacteur"
    id: Mapped[int] = mapped_column("id_redacteur", primary_key=True)
    name: Mapped[str] = mapped_column("redacteur_nom")


class BibTechniquesMob(db.Model):
    __tablename__ = "bib_mob_img_techniques"
    id: Mapped[int] = mapped_column("id_technique", primary_key=True)
    name: Mapped[str] = mapped_column("technique_type")


class BibNaturesPersonnesMorales(db.Model):
    __tablename__ = "bib_pers_mo_natures"
    id: Mapped[int] = mapped_column("id_pers_mo_nature", primary_key=True)
    name: Mapped[str] = mapped_column("pers_mo_nature_type")


class BibProfessions(db.Model):
    __tablename__ = "bib_pers_phy_professions"
    id: Mapped[int] = mapped_column("id_profession", primary_key=True)
    name: Mapped[str] = mapped_column("profession_type")


class BibDeplacements(db.Model):
    __tablename__ = "bib_pers_phy_modes_deplacements"
    id: Mapped[int] = mapped_column("id_mode_deplacement", primary_key=True)
    name: Mapped[str] = mapped_column("mode_deplacement_type")


class BibPerdiodesHisto(db.Model):
    __tablename__ = "bib_pers_phy_periodes_historiques"
    id: Mapped[int] = mapped_column("id_periode_historique", primary_key=True)
    name: Mapped[str] = mapped_column("periode_historique_type")


class Pays(db.Model):
    __tablename__ = "loc_pays"
    id: Mapped[int] = mapped_column("id_pays", primary_key=True)
    name: Mapped[str] = mapped_column("nom_pays")


class Region(db.Model):
    __tablename__ = "loc_regions"
    id: Mapped[int] = mapped_column("id_region", primary_key=True)
    name: Mapped[str] = mapped_column("nom_region")
    id_pays: Mapped[int] = mapped_column(ForeignKey("loc_pays.id_pays"))
    pays: Mapped[Pays] = relationship()


class Departement(db.Model):
    __tablename__ = "loc_departements"
    id: Mapped[int] = mapped_column("id_departement", primary_key=True)
    name: Mapped[str] = mapped_column("nom_departement")
    id_region: Mapped[int] = mapped_column(ForeignKey("loc_regions.id_region"))
    region: Mapped[Region] = relationship()


class Commune(db.Model):
    __tablename__ = "loc_communes"
    id: Mapped[int] = mapped_column("id_commune", primary_key=True)
    name: Mapped[str] = mapped_column("nom_commune")
    id_departement: Mapped[str] = mapped_column(
        ForeignKey("loc_departements.id_departement")
    )
    departement: Mapped[Departement] = relationship()


class CategorieSelect(Select):
    inherit_cache = True

    def auto_joinload(self, model, fields=[]):
        query_option = [raiseload("*")]
        for f in fields:
            if f in model.__mapper__.relationships:
                query_option.append(joinedload(getattr(model, f)))
        if "departement" in fields or "region" in fields:
            self = self.options(
                joinedload(model.commune)
                .joinedload(Commune.departement)
                .joinedload(Departement.region)
            )
        self = self.options(*tuple(query_option))
        return self

    def where_has_media(self, model):
        return self.filter(model.medias.any())

    def auto_filters(self, params, model, remove_publish=True):
        """
        BECAUSE OF manuel join, we CANNOT use .filter_by option
        """
        join_on_geo = False
        if "has_medias" in params and params["has_medias"] == "true":
            params.pop("has_medias")
            self = self.filter(model.medias.any())
        if "siecles" in params:
            if hasattr(model, "siecles"):
                siecles = params.getlist("siecles")
                self = self.filter(model.siecles.any(BibSiecle.id.in_(siecles)))

        if "pays" in params:
            if hasattr(model, "id_pays"):
                self = self.filter(model.id_pays.in_(params.getlist("pays")))

        if "communes" in params:
            if hasattr(model, "id_commune"):
                self = self.filter(model.id_commune.in_(params.getlist("communes")))
        if "departements" in params:
            departements = params.getlist("departements")
            self = self.join(Commune).join(Departement)

            self = self.filter(Departement.id.in_(departements))
            join_on_geo = True
        if "regions" in params:
            regions = params.getlist("regions")
            if join_on_geo:
                self = self.join(Region)
            else:
                self = self.join(Commune).join(Departement).join(Region)
            self = self.filter(Region.id.in_(regions))

        if "etats_conservation" in params:
            if hasattr(model, "etat_conservation"):
                etats_conservation = params.getlist("etats_conservation")
                self = self.filter(
                    model.etat_conservation.any(
                        BibEtatConservation.id.in_(etats_conservation)
                    )
                )
        if "natures_pers" in params:
            if hasattr(model, "natures"):
                natures = params.getlist("natures_pers")
                self = self.filter(
                    model.natures.any(BibNaturesPersonnesMorales.id.in_(natures))
                )
        if "natures_monu" in params:
            if hasattr(model, "natures"):
                natures = params.getlist("natures_pers")
                self = self.filter(model.natures.any(BibMonuLieuNature.id.in_(natures)))

        if "modes_deplacement" in params:
            if hasattr(model, "modes_deplacement"):
                modes_deplacements = params.getlist("modes_deplacement")
                self = self.filter(
                    model.modes_deplacements.any(
                        BibDeplacements.id.in_(modes_deplacements)
                    )
                )
        if "professions" in params:
            if hasattr(model, "professions"):
                professions = params.getlist("professions")
                self = self.filter(
                    model.professions.any(BibProfessions.id.in_(professions))
                )
        if "designations" in params:
            if hasattr(model, "designations"):
                designations = params.getlist("designations")
                self = self.filter(
                    model.designations.any(BibDesignationMobImg.id.in_(designations))
                )
        if "techniques" in params:
            if hasattr(model, "techniques"):
                techniques = params.getlist("techniques")
                self = self.filter(
                    model.techniques.any(BibTechniquesMob.id.in_(techniques))
                )

        if "random" in params:
            self = self.order_by(func.random())
        if "limit" in params:
            self = self.limit(params.pop("limit"))

        # force publish
        if remove_publish:
            self = self.filter(model.publie == True)
        return self


class MobilierImage(db.Model):
    __tablename__ = "t_mobiliers_images"
    __select_class__ = CategorieSelect

    id: Mapped[int] = mapped_column("id_mobilier_image", primary_key=True)
    title: Mapped[str] = mapped_column("titre_mob_img")
    description: Mapped[str] = mapped_column()
    histoire: Mapped[str] = mapped_column("historique")
    source: Mapped[str] = mapped_column("source")
    bibliographie: Mapped[str] = mapped_column()
    date_creation: Mapped[str] = mapped_column()
    date_maj: Mapped[str] = mapped_column()
    publie: Mapped[bool] = mapped_column()
    id_pays: Mapped[int] = mapped_column(ForeignKey("loc_pays.id_pays"))
    id_commune: Mapped[int] = mapped_column(ForeignKey("loc_communes.id_commune"))

    medias: Mapped[List[Media]] = relationship(secondary=cor_medias_mob_img)

    etats_conservation: Mapped[List[BibEtatConservation]] = relationship(
        secondary=cor_etat_cons_mob_img
    )
    designations: Mapped[List[BibDesignationMobImg]] = relationship(
        secondary=cor_designations_mob_img
    )
    techniques: Mapped[List[BibTechniquesMob]] = relationship(
        secondary=cor_techniques_mob_img
    )
    materiaux: Mapped[List[BibMateriaux]] = relationship(
        secondary=cor_materiaux_mob_img
    )
    auteurs: Mapped[List[BibSourceAuteur]] = relationship(
        secondary=cor_source_auteur_mob_img
    )
    contributeurs: Mapped[List[BibContributeur]] = relationship(
        secondary=cor_contributeurs_mob_img
    )
    redacteurs: Mapped[List[BibRedacteur]] = relationship(
        secondary=cor_redacteurs_mob_img
    )

    siecles: Mapped[List[BibSiecle]] = relationship(secondary=cor_siecles_mob_img)
    pays: Mapped[List[Pays]] = relationship()
    commune: Mapped[List[Commune]] = relationship()
    personnes_morales_liees: Mapped[List["PersonneMorale"]] = relationship(
        secondary=cor_mob_img_pers_mo, back_populates="mobiliers_images_liees"
    )
    monuments_lieux_liees: Mapped[List["MonumentLieu"]] = relationship(
        secondary=cor_monu_lieu_mob_img, back_populates="mobiliers_images_liees"
    )


class PersonneMorale(db.Model):
    __tablename__ = "t_pers_morales"
    __select_class__ = CategorieSelect

    id: Mapped[int] = mapped_column("id_pers_morale", primary_key=True)
    title: Mapped[str] = mapped_column("titre_pers_mo")
    source: Mapped[str] = mapped_column("sources")
    historique: Mapped[str] = mapped_column("historique")
    statuts: Mapped[str] = mapped_column("statuts")
    texte_statuts: Mapped[str] = mapped_column("texte_statuts")
    commentaires: Mapped[str] = mapped_column("commentaires")
    acte_fondation: Mapped[bool] = mapped_column("acte_fondation")
    bibliographie: Mapped[str] = mapped_column()
    date_creation: Mapped[str] = mapped_column()
    date_maj: Mapped[str] = mapped_column()
    publie: Mapped[bool] = mapped_column()
    id_pays: Mapped[int] = mapped_column(ForeignKey("loc_pays.id_pays"))
    id_commune: Mapped[int] = mapped_column(ForeignKey("loc_communes.id_commune"))

    medias: Mapped[List[Media]] = relationship(secondary=cor_medias_pers_mo)
    natures: Mapped[List[BibNaturesPersonnesMorales]] = relationship(
        secondary=cor_natures_pers_mo
    )
    contributeurs: Mapped[List[BibContributeur]] = relationship(
        secondary=cor_contributeurs_pers_mo
    )
    redacteurs: Mapped[List[BibRedacteur]] = relationship(
        secondary=cor_redacteurs_pers_mo
    )

    siecles: Mapped[List[BibSiecle]] = relationship(secondary=cor_siecles_pers_mo)
    pays: Mapped[List[Pays]] = relationship()
    commune: Mapped[List[Commune]] = relationship()

    personnes_physiques_liees: Mapped[List["PersonnePhysique"]] = relationship(
        secondary=cor_pers_phy_pers_mo, back_populates="personnes_morales_liees"
    )

    monuments_lieux_liees: Mapped[List["MonumentLieu"]] = relationship(
        secondary=cor_monu_lieu_pers_mo, back_populates="personnes_morales_liees"
    )

    mobiliers_images_liees: Mapped[List[MobilierImage]] = relationship(
        secondary=cor_mob_img_pers_mo
    )


class PersonnePhysique(db.Model):
    __tablename__ = "t_pers_physiques"
    __select_class__ = CategorieSelect

    id: Mapped[int] = mapped_column("id_pers_physique", primary_key=True)
    prenom_nom_pers_phy: Mapped[str] = mapped_column()
    source: Mapped[str] = mapped_column("sources")
    date_creation: Mapped[str] = mapped_column()
    elements_biographiques: Mapped[str] = mapped_column()
    nature_evenement: Mapped[str] = mapped_column()
    commutation_voeu: Mapped[str] = mapped_column()
    elements_pelerinage: Mapped[str] = mapped_column()
    attestation: Mapped[str] = mapped_column()
    date_maj: Mapped[str] = mapped_column()
    publie: Mapped[bool] = mapped_column()
    bibliographie: Mapped[str]
    id_pays: Mapped[int] = mapped_column(ForeignKey("loc_pays.id_pays"))
    id_commune: Mapped[int] = mapped_column(ForeignKey("loc_communes.id_commune"))

    medias: Mapped[List[Media]] = relationship(secondary=cor_medias_pers_phy)
    modes_deplacements: Mapped[List[BibDeplacements]] = relationship(
        secondary=cor_modes_deplacements_pers_phy
    )
    professions: Mapped[List[BibProfessions]] = relationship(
        secondary=cor_professions_pers_phy
    )
    contributeurs: Mapped[List[BibContributeur]] = relationship(
        secondary=cor_contributeurs_pers_phy
    )
    redacteurs: Mapped[List[BibRedacteur]] = relationship(
        secondary=cor_redacteurs_pers_phy
    )
    periodes_historiques: Mapped[List[BibPerdiodesHisto]] = relationship(
        secondary=cor_periodes_historiques_pers_phy
    )
    personnes_morales_liees: Mapped[List[PersonneMorale]] = relationship(
        secondary=cor_pers_phy_pers_mo, back_populates="personnes_physiques_liees"
    )

    monuments_lieux_liees: Mapped[List["MonumentLieu"]] = relationship(
        secondary=cor_monu_lieu_pers_phy, back_populates="personnes_physiques_liees"
    )

    siecles: Mapped[List[BibSiecle]] = relationship(secondary=cor_siecles_pers_phy)
    pays: Mapped[List[Pays]] = relationship()
    commune: Mapped[List[Commune]] = relationship()


class MonumentLieu(db.Model):
    __tablename__ = "t_monuments_lieux"
    __select_class__ = CategorieSelect

    id: Mapped[int] = mapped_column("id_monument_lieu", primary_key=True)
    title: Mapped[str] = mapped_column("titre_monu_lieu")
    description: Mapped[str] = mapped_column()
    histoire: Mapped[str] = mapped_column()
    source: Mapped[str]
    protection: Mapped[str] = mapped_column()
    bibliographie: Mapped[str] = mapped_column()
    geolocalisation: Mapped[str]
    date_creation: Mapped[str] = mapped_column()
    date_maj: Mapped[str] = mapped_column()
    publie: Mapped[bool] = mapped_column()
    id_pays: Mapped[int] = mapped_column(ForeignKey("loc_pays.id_pays"))
    id_commune: Mapped[int] = mapped_column(ForeignKey("loc_communes.id_commune"))

    pays: Mapped[List[Pays]] = relationship()
    commune: Mapped[List[Commune]] = relationship()
    siecles: Mapped[List[BibSiecle]] = relationship(secondary=cor_siecles_monu_lieu)

    natures: Mapped[List[BibMonuLieuNature]] = relationship(
        secondary=cor_natures_monu_lieu
    )
    etats_conservation: Mapped[List[BibEtatConservation]] = relationship(
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
    mobiliers_images_liees: Mapped[List[MobilierImage]] = relationship(
        secondary=cor_monu_lieu_mob_img
    )

    personnes_morales_liees: Mapped[List[PersonneMorale]] = relationship(
        secondary=cor_monu_lieu_pers_mo, back_populates="monuments_lieux_liees"
    )
    personnes_physiques_liees: Mapped[List[PersonnePhysique]] = relationship(
        secondary=cor_monu_lieu_pers_phy
    )
