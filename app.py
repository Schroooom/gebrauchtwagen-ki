import streamlit as st
import openai

st.set_page_config(page_title="KI-Gebrauchtwagen-Berater", page_icon="🚗")

st.title("🚗 Dein KI-gestützter Gebrauchtwagen-Berater")
st.write("Füttere den Berater mit deinen Wünschen, und die KI sucht die perfekten Autos für dich heraus.")

# Seitenleiste für den API-Schlüssel (damit er sicher bleibt)
st.sidebar.header("🔑 Einstellungen")
api_key_input = st.sidebar.text_input("OpenAI API-Key eingeben:", type="password")

# Eingabemasken für den Nutzer
with st.form("car_form"):
    budget = st.slider("Wie hoch ist dein Budget in Euro?", 3000, 50000, 12000, step=1000)
    groesse = st.selectbox("Wie groß soll das Auto sein?", ["Kleinwagen", "Kompaktklasse (Golf-Größe)", "Kombi / Familienauto", "SUV"])
    kilometer = st.number_input("Wie viele Kilometer fährst du ca. pro Jahr?", min_value=1000, max_value=50000, value=12000, step=1000)
    strecke = st.selectbox("Was für Strecken fährst du hauptsächlich?", ["Hauptsächlich Stadt / Kurzstrecke", "Mischung (Stadt & Land)", "Hauptsächlich Autobahn / Langstrecke"])
    sonstiges = st.text_input("Besondere Wünsche? (z.B. Automatik, Sitzheizung, Marke X)", "Keine besonderen Wünsche")
    
    submit_button = st.form_submit_button(label="KI-Empfehlung generieren")

# Wenn der Button geklickt wird
if submit_button:
    if not api_key_input:
        st.error("Bitte gib zuerst deinen OpenAI API-Key in der Seitenleiste links ein!")
    else:
        with st.spinner("Die KI analysiert den Gebrauchtwagenmarkt für dich..."):
            try:
                # OpenAI Client initialisieren
                client = openai.OpenAI(api_key=api_key_input)
                
                # Den Prompt (die Anweisung) für die KI zusammenbauen
                prompt = f"""
                Du bist ein erfahrener, unabhängiger Gebrauchtwagen-Experte und Kfz-Meister.
                Empfiehl dem Nutzer genau 2-3 passende Automodelle basierend auf folgenden Daten:
                - Budget: {budget} Euro
                - Fahrzeuggröße: {groesse}
                - Fahrleistung: {kilometer} km pro Jahr
                - Fahrprofil: {strecke}
                - Extrawünsche: {sonstiges}
                
                Gib für jedes empfohlene Modell an:
                1. Modellname und ca. Baujahre in diesem Preisbereich
                2. Welcher Motor (Benzin/Diesel/Hybrid) am besten passt und warum
                3. Worauf man beim Gebrauchtwagenkauf dieses Modells besonders achten muss (typische Schwachstellen).
                Formatiere die Antwort übersichtlich mit Aufzählungen.
                """
                
                # Anfrage an das Sprachmodell senden
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # Kosteneffizientes und schnelles Modell
                    messages=[
                        {"role": "system", "content": "Du bist ein hilfsbereiter, kompetenter Auto-Experte."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                
                # Ergebnis anzeigen
                st.subheader("💡 KI-Empfehlung für dich:")
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Ein Fehler ist aufgetreten: {e}")