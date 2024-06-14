
# app.py
import streamlit as st
import data

st.set_page_config(page_title="Enquête Emploi ménage", page_icon="👗", layout="wide")

st.sidebar.title("Menu")
page = st.sidebar.selectbox("Choisir une page",
                                ["Enregistrer ZD","Performance Equipe","Rapport statistique"])


equipe=["Equipe 1","Equipe 2","Equipe 3","Equipe 4","Equipe 5","Equipe 6",]
# Initialisation de l'état de confirmation pour la suppression
if 'confirm_delete' not in st.session_state:
    st.session_state.confirm_delete = None

if 'edit_performance' not in st.session_state:
    st.session_state.edit_performance = {}
# Titre de l'application
st.title("Application de suivi ")

if page=="Enregistrer ZD":
    # Section pour enregistrer une nouvelle zone de dénombrement
    st.header("Enregistrer une nouvelle Zone de Dénombrement")

    with st.form("zone_denombrement_form"):
        region = st.text_input("Région")
        departement = st.text_input("Département")
        sous_prefecture = st.text_input("Sous-préfecture")
        zone_D = st.text_input("Zone de Dénombrement")
        submitted = st.form_submit_button("Enregistrer")

        if submitted:
            if region and departement and sous_prefecture and zone_D:
                if data.enregistrer_zone_denombrement(region, departement, sous_prefecture, zone_D):
                    st.success("Zone de Dénombrement enregistrée avec succès.")
                else:
                    st.error("Cette Zone de Dénombrement existe déjà.")
            else:
                st.error("Veuillez remplir tous les champs.")
elif page=="Rapport statistique":
    st.header("Rapport statistique")
    stats_equipe, stats_zone_D =data.generer_rapport()

    st.header("Statistiques par Équipe")
    st.dataframe(stats_equipe)

    st.header("Statistiques par Zone de Dénombrement")
    st.dataframe(stats_zone_D)

    # Statistiques de refus
    st.header("Statistiques de Refus")
    performances=data.obtenir_performances()
    stats_refus = performances.groupby('Zone de Dénombrement').agg({
        'Nombre de Ménages Ayant Refusé': 'sum',
        'Nombre d’Individus Ayant Refusé': 'sum'
    }).reset_index()
    st.dataframe(stats_refus)

    # Taille des ménages
    st.header("Taille des Ménages Enquêtés")
    stats_menage = performances.groupby('Zone de Dénombrement').agg({
        'Nombre de Ménages Enquêtés': 'sum',
        'Nombre d’Individus dans les Ménages Enquêtés': 'sum'
    }).reset_index()
    stats_menage['Taille Moyenne des Ménages'] = stats_menage['Nombre d’Individus dans les Ménages Enquêtés'] / \
                                                 stats_menage['Nombre de Ménages Enquêtés']
    st.dataframe(stats_menage)


else:
    if st.checkbox("Statistique pour nouvelle ZD"):

        st.markdown('<h2 style="color: blue;">Enregistrer une nouvelle statistique</h2>', unsafe_allow_html=True)

        with st.form("performance_form"):
            region = st.selectbox("Choisir la région",options=data.obtenir_region())
            departement = st.selectbox("Choisir le département",options=data.obtenir_departement())
            sous_prefecture = st.selectbox("Choisir la sous-préfecture", options=data.obtenir_sous_prefecture())
            zone_D = st.selectbox("Choisir la Zone de Dénombrement",options=data.obtenir_zone_D())
            equipe = st.selectbox("Choisir votre Équipe",options=equipe)
            segment_total = st.number_input("Segment Total", min_value=0)
            segment_acheve = st.number_input("Segment Achevé", min_value=0)
            segment_restant = st.number_input("Segment Restant", min_value=0)
            nbre_menage_denombrer = st.number_input("Nombre de Ménages à Dénombrer", min_value=0)
            nbre_menage_enquete = st.number_input("Nombre de Ménages Enquêtés", min_value=0)
            nbre_individu_dans_menage_enquete = st.number_input("Nombre d’Individus dans les Ménages Enquêtés", min_value=0)
            nbre_menage_absent = st.number_input("Nombre de Ménages Absents", min_value=0)
            nbre_menage_ayant_refus = st.number_input("Nombre de Ménages Ayant Refusé", min_value=0)
            nbre_individu_enquete_section_emploi = st.number_input("Nombre d’Individus Enquêtés (Section Emploi)", min_value=0)
            nbre_individu_refus = st.number_input("Nombre d’Individus Ayant Refusé", min_value=0)
            observation = st.text_area("Observation")
            submitted = st.form_submit_button("Enregistrer")

            if submitted:
                if region and departement and sous_prefecture and zone_D and equipe:
                    data.enregistrer_performance(region, departement, sous_prefecture, zone_D, equipe, segment_total, segment_acheve, segment_restant,
                                                 nbre_menage_denombrer, nbre_menage_enquete, nbre_individu_dans_menage_enquete,
                                                 nbre_menage_absent, nbre_menage_ayant_refus, nbre_individu_enquete_section_emploi,
                                                 nbre_individu_refus, observation)
                    st.success("Statistique enregistrée avec succès.")
                else:
                    st.error("Vous n'avez pas rempli région ou departement ou Zone de denombrement ou Equipe")


    elif st.checkbox("Mise à jour ZD"):
            # Section pour afficher et modifier les performances enregistrées
        st.markdown('<h2 style="color: blue;">Mise à jour de la statistique</h2>', unsafe_allow_html=True)

        performance_data = data.obtenir_performances()
        if st.checkbox("Afficher les ZD à modifier"):
            if not performance_data.empty:
                for index, row in performance_data.iterrows():
                    col1, col2 = st.columns(2)
                    if st.checkbox(f"Afficher la ZD {row['Zone de Dénombrement']} {row['Sous-préfecture']}" ,key=f"formulaire_{row['ID']}"):
                        with col1:
                            st.write("Sous-préfecture de :", row['Sous-préfecture'])
                            st.write("ZD", row['Zone de Dénombrement'])
                            if st.button(f"Modifier", key=f"modifier_{row['ID']}"):
                                st.session_state.edit_performance[row['ID']] = True

                        if st.session_state.edit_performance.get(row['ID'], False):
                            with st.form(f"modifier_form_{row['ID']}"):
                                region = st.text_input("Région", value=row['Région'])
                                departement = st.text_input("Département", value=row['Département'])
                                sous_prefecture = st.text_input("Sous-préfecture", value=row['Sous-préfecture'])
                                zone_D = st.text_input("Zone de Dénombrement", value=row['Zone de Dénombrement'])
                                equipe = st.text_input("Équipe", value=row['Équipe'])
                                segment_total = st.number_input("Segment Total", min_value=0, value=row['Segment Total'])
                                segment_acheve = st.number_input("Segment Achevé", min_value=0, value=row['Segment Achevé'])
                                segment_restant = st.number_input("Segment Restant", min_value=0, value=row['Segment Restant'])
                                nbre_menage_denombrer = st.number_input("Nombre de Ménages à Dénombrer", min_value=0,
                                                                        value=row['Nombre de Ménages à Dénombrer'])
                                nbre_menage_enquete = st.number_input("Nombre de Ménages Enquêtés", min_value=0,
                                                                      value=row['Nombre de Ménages Enquêtés'])
                                nbre_individu_dans_menage_enquete = st.number_input("Nombre d’Individus dans les Ménages Enquêtés",
                                                                                    min_value=0, value=row[
                                        'Nombre d’Individus dans les Ménages Enquêtés'])
                                nbre_menage_absent = st.number_input("Nombre de Ménages Absents", min_value=0,
                                                                     value=row['Nombre de Ménages Absents'])
                                nbre_menage_ayant_refus = st.number_input("Nombre de Ménages Ayant Refusé", min_value=0,
                                                                          value=row['Nombre de Ménages Ayant Refusé'])
                                nbre_individu_enquete_section_emploi = st.number_input(
                                    "Nombre d’Individus Enquêtés (Section Emploi)", min_value=0,
                                    value=row['Nombre d’Individus Enquêtés (Section Emploi)'])
                                nbre_individu_refus = st.number_input("Nombre d’Individus Ayant Refusé", min_value=0,
                                                                      value=row['Nombre d’Individus Ayant Refusé'])
                                observation = st.text_area("Observation", value=row['Observation'])
                                submitted = st.form_submit_button("Modifier")

                                if submitted:
                                    data.modifier_performance(row['ID'], region, departement, sous_prefecture, zone_D, equipe,
                                                              segment_total, segment_acheve, segment_restant,
                                                              nbre_menage_denombrer, nbre_menage_enquete,
                                                              nbre_individu_dans_menage_enquete,
                                                              nbre_menage_absent, nbre_menage_ayant_refus,
                                                              nbre_individu_enquete_section_emploi,
                                                              nbre_individu_refus, observation)
                                    st.session_state.edit_performance[row['ID']] = False
                                    st.experimental_rerun()

                                    st.success("Performance modifiée avec succès.")
    else:                                # Refresh the page to show updated data


        st.info("En attente de statistique....")



