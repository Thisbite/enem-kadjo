# data.py

import sqlite3
import pandas as pd

# Connexion à la base de données
conn = sqlite3.connect("ene_M.db")
cursor = conn.cursor()

def create_table():
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS zone_denombrement(
            id INTEGER PRIMARY KEY,
            region TEXT,
            departement TEXT,
            sous_prefecture TEXT,
            zone_D TEXT,
            UNIQUE(region, departement, sous_prefecture, zone_D) -- Ajout d'une contrainte UNIQUE
        )
        '''
    )
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS performances(
            id INTEGER PRIMARY KEY,
            region TEXT,
            departement TEXT,
            sous_prefecture TEXT,
            zone_D TEXT,
            equipe TEXT,
            segment_total INTEGER,
            segment_acheve INTEGER,
            segment_restant INTEGER,
            nbre_menage_denombrer INTEGER,
            nbre_menage_enquete INTEGER,
            nbre_individu_dans_menage_enquete INTEGER,
            nbre_menage_absent INTEGER,
            nbre_menage_ayant_refus INTEGER,
            nbre_individu_enquete_section_emploi INTEGER,
            nbre_individu_refus INTEGER,
            observation TEXT
        )
        '''
    )



    conn.commit()

def verifier_doublon(region, departement, sous_prefecture, zone_D):
    cursor.execute(
        '''
        SELECT COUNT(*) FROM zone_denombrement
        WHERE region=? AND departement=? AND sous_prefecture=? AND zone_D=?
        ''', (region, departement, sous_prefecture, zone_D)
    )
    return cursor.fetchone()[0] > 0

def enregistrer_zone_denombrement(region, departement, sous_prefecture, zone_D):
    if verifier_doublon(region, departement, sous_prefecture, zone_D):
        return False  # Indiquer que la zone de dénombrement existe déjà
    cursor.execute(
        '''
        INSERT INTO zone_denombrement(region, departement, sous_prefecture, zone_D)
        VALUES (?, ?, ?, ?)
        ''', (region, departement, sous_prefecture, zone_D)
    )
    conn.commit()
    return True

def obtenir_zone_D():
    cursor.execute('SELECT * FROM zone_denombrement')
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['ID', 'Région', 'Département', 'Sous-préfecture', 'Zone de dénombrement'])
    return df

def supprimer_zone_denombrement(zone_id):
    cursor.execute('DELETE FROM zone_denombrement WHERE id=?', (zone_id,))
    conn.commit()

def modifier_zone_denombrement(zone_id, region, departement, sous_prefecture, zone_D):
    cursor.execute(
        '''
        UPDATE zone_denombrement
        SET region=?, departement=?, sous_prefecture=?, zone_D=?
        WHERE id=?
        ''', (region, departement, sous_prefecture, zone_D, zone_id)
    )
    conn.commit()




def enregistrer_performance(region, departement, sous_prefecture, zone_D, equipe, segment_total, segment_acheve, segment_restant,
                            nbre_menage_denombrer, nbre_menage_enquete, nbre_individu_dans_menage_enquete,
                            nbre_menage_absent, nbre_menage_ayant_refus, nbre_individu_enquete_section_emploi,
                            nbre_individu_refus, observation):
    cursor.execute(
        '''
        INSERT INTO performances(region, departement, sous_prefecture, zone_D, equipe, segment_total, segment_acheve, segment_restant,
                                nbre_menage_denombrer, nbre_menage_enquete, nbre_individu_dans_menage_enquete, nbre_menage_absent, 
                                nbre_menage_ayant_refus, nbre_individu_enquete_section_emploi, nbre_individu_refus, observation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (region, departement, sous_prefecture, zone_D, equipe, segment_total, segment_acheve, segment_restant,
              nbre_menage_denombrer, nbre_menage_enquete, nbre_individu_dans_menage_enquete, nbre_menage_absent,
              nbre_menage_ayant_refus, nbre_individu_enquete_section_emploi, nbre_individu_refus, observation)
    )
    conn.commit()

def obtenir_performances():
    cursor.execute('SELECT * FROM performances')
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=[
        'ID', 'Région', 'Département', 'Sous-préfecture', 'Zone de Dénombrement', 'Équipe', 'Segment Total', 'Segment Achevé',
        'Segment Restant', 'Nombre de Ménages à Dénombrer', 'Nombre de Ménages Enquêtés', 'Nombre d’Individus dans les Ménages Enquêtés',
        'Nombre de Ménages Absents', 'Nombre de Ménages Ayant Refusé', 'Nombre d’Individus Enquêtés (Section Emploi)',
        'Nombre d’Individus Ayant Refusé', 'Observation'
    ])
    return df

def modifier_performance(id, region, departement, sous_prefecture, zone_D, equipe, segment_total, segment_acheve, segment_restant,
                         nbre_menage_denombrer, nbre_menage_enquete, nbre_individu_dans_menage_enquete,
                         nbre_menage_absent, nbre_menage_ayant_refus, nbre_individu_enquete_section_emploi,
                         nbre_individu_refus, observation):
    cursor.execute(
        '''
        UPDATE performances
        SET region=?, departement=?, sous_prefecture=?, zone_D=?, equipe=?, segment_total=?, segment_acheve=?, segment_restant=?, 
            nbre_menage_denombrer=?, nbre_menage_enquete=?, nbre_individu_dans_menage_enquete=?, nbre_menage_absent=?, 
            nbre_menage_ayant_refus=?, nbre_individu_enquete_section_emploi=?, nbre_individu_refus=?, observation=?
        WHERE id=?
        ''', (region, departement, sous_prefecture, zone_D, equipe, segment_total, segment_acheve, segment_restant,
              nbre_menage_denombrer, nbre_menage_enquete, nbre_individu_dans_menage_enquete, nbre_menage_absent,
              nbre_menage_ayant_refus, nbre_individu_enquete_section_emploi, nbre_individu_refus, observation, id)
    )
    conn.commit()

# Créer la table lors de l'importation du module
create_table()



def obtenir_region():
    cursor.execute('SELECT DISTINCT region FROM zone_denombrement')
    data = cursor.fetchall()
    regions = [row[0] for row in data]  # Extraire les régions des tuples
    return regions

def obtenir_departement():
    cursor.execute('SELECT DISTINCT departement FROM zone_denombrement')
    data = cursor.fetchall()
    departement = [row[0] for row in data]  # Extraire les régions des tuples
    return departement



def obtenir_sous_prefecture():
    cursor.execute('SELECT DISTINCT sous_prefecture FROM zone_denombrement')
    data = cursor.fetchall()
    sous_prefecture = [row[0] for row in data]  # Extraire les régions des tuples
    return sous_prefecture



def obtenir_zone_D():
    cursor.execute('SELECT DISTINCT zone_D FROM zone_denombrement')
    data = cursor.fetchall()
    zone_D = [row[0] for row in data]  # Extraire les régions des tuples
    return zone_D


"""
Rapport statitisque

"""
# Fonction pour générer le rapport statistique
def generer_rapport():
    performances =obtenir_performances()

    # Statistiques par équipe
    stats_equipe = performances.groupby('Équipe').agg({
        'ID': 'count',
        'Segment Total': 'sum',
        'Segment Achevé': 'sum',
        'Segment Restant': 'sum',
        'Nombre de Ménages à Dénombrer': 'sum',
        'Nombre de Ménages Enquêtés': 'sum',
        'Nombre d’Individus dans les Ménages Enquêtés': 'sum',
        'Nombre de Ménages Absents': 'sum',
        'Nombre de Ménages Ayant Refusé': 'sum',
        'Nombre d’Individus Enquêtés (Section Emploi)': 'sum',
        'Nombre d’Individus Ayant Refusé': 'sum'
    }).reset_index().rename(columns={'ID': 'Nombre de ZD effectuées'})

    # Statistiques par Zone de Dénombrement
    stats_zone_D = performances.groupby('Zone de Dénombrement').agg({
        'ID': 'count',
        'Segment Total': 'sum',
        'Segment Achevé': 'sum',
        'Segment Restant': 'sum',
        'Nombre de Ménages à Dénombrer': 'sum',
        'Nombre de Ménages Enquêtés': 'sum',
        'Nombre d’Individus dans les Ménages Enquêtés': 'sum',
        'Nombre de Ménages Absents': 'sum',
        'Nombre de Ménages Ayant Refusé': 'sum',
        'Nombre d’Individus Enquêtés (Section Emploi)': 'sum',
        'Nombre d’Individus Ayant Refusé': 'sum'
    }).reset_index().rename(columns={'ID': 'Nombre de Performances'})

    return stats_equipe, stats_zone_D

