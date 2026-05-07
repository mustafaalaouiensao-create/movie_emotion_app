import streamlit as st
from db_connection import get_collection
from nlp_model import analyze_user_text
from recommender import get_recommendations, get_recommendations_by_emotion
from views import show_movie_row, show_movies_ai
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Configuration ---
st.set_page_config(page_title="Movie Sentiment AI", layout="wide")
collection = get_collection()

# --- Fonctions ---

def send_email(name, email, message):
    try:
        sender     = ""      
        password   = ""         
        receiver   = "lm0358@gmail.com"        

        msg = MIMEMultipart()
        msg["From"]    = sender
        msg["To"]      = receiver
        msg["Subject"] = f"📩 Nouveau message de {name} - Movie Sentiment AI"

        body = f"""
        Nouveau message reçu sur Movie Sentiment AI :
        
        👤 Nom    : {name}
        📧 Email  : {email}
        
        💬 Message :
        {message}
        """
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
        return True
    except Exception as e:
        print(f"Erreur email : {e}")
        return False
    
def search_movies(collection, query):
    return list(collection.find({
        "title": {"$regex": query, "$options": "i"}
    }).limit(10))

def get_image_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def get_random_posters(collection, n=8):
    pipeline = [
        {"$match": {"poster_url": {"$exists": True, "$ne": None, "$ne": ""}}},
        {"$sample": {"size": n}},
        {"$project": {"poster_url": 1, "_id": 0}}
    ]
    results = list(collection.aggregate(pipeline))
    return [r["poster_url"] for r in results]

# --- Assets ---
logo_base64 = get_image_base64("Monlogo.png")
posters = get_random_posters(collection, n=8)

positions = [
    ("2%",  "5%"),  ("14%", "55%"), ("26%", "10%"), ("38%", "60%"),
    ("52%", "8%"),  ("63%", "58%"), ("75%", "12%"), ("87%", "50%")
]
rotations = [-10, 7, -6, 10, -8, 6, -7, 9]

posters_html = ""
for i, poster in enumerate(posters):
    left, top = positions[i % len(positions)]
    rotation = rotations[i % len(rotations)]
    posters_html += (
        f'<img src="{poster}" '
        f'style="position:absolute; left:{left}; top:{top}; height:170px; '
        f'opacity:0.22; border-radius:8px; transform:rotate({rotation}deg); '
        f'filter:blur(0.3px) grayscale(10%); pointer-events:none; '
        f'box-shadow:0 4px 15px rgba(0,0,0,0.5);" '
        f'onerror="this.style.display=\'none\'"/>'
    )

# --- CSS GLOBAL ---
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        max-width: 100% !important;
    }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stVerticalBlock"] { position: relative; z-index: 1; }
    body { margin: 0; font-family: 'Segoe UI', sans-serif; }

    [data-testid="stAppViewContainer"] {
        background: #020c1b;
        background-attachment: fixed;
    }
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background-image:
            radial-gradient(1px 1px at 5%  10%, rgba(0,196,255,0.6) 0%, transparent 100%),
            radial-gradient(1px 1px at 15% 35%, rgba(255,255,255,0.4) 0%, transparent 100%),
            radial-gradient(1px 1px at 25% 60%, rgba(0,196,255,0.5) 0%, transparent 100%),
            radial-gradient(1px 1px at 35% 20%, rgba(255,255,255,0.3) 0%, transparent 100%),
            radial-gradient(1px 1px at 45% 75%, rgba(0,196,255,0.4) 0%, transparent 100%),
            radial-gradient(1px 1px at 55% 40%, rgba(255,255,255,0.3) 0%, transparent 100%),
            radial-gradient(1px 1px at 65% 85%, rgba(0,196,255,0.6) 0%, transparent 100%),
            radial-gradient(1px 1px at 75% 15%, rgba(255,255,255,0.4) 0%, transparent 100%),
            radial-gradient(1px 1px at 85% 55%, rgba(0,196,255,0.5) 0%, transparent 100%),
            radial-gradient(1px 1px at 95% 30%, rgba(255,255,255,0.3) 0%, transparent 100%),
            radial-gradient(2px 2px at 20% 20%, rgba(255,204,0,0.4) 0%, transparent 100%),
            radial-gradient(2px 2px at 50% 50%, rgba(0,196,255,0.4) 0%, transparent 100%),
            radial-gradient(2px 2px at 80% 30%, rgba(255,204,0,0.3) 0%, transparent 100%);
        pointer-events: none;
        z-index: 0;
        animation: twinkle 4s infinite alternate ease-in-out;
    }
    @keyframes twinkle {
        0%   { opacity: 0.3; }
        50%  { opacity: 0.9; }
        100% { opacity: 0.4; }
    }
    [data-testid="stAppViewContainer"]::after {
        content: '';
        position: fixed;
        bottom: 0; left: 0;
        width: 100%; height: 200px;
        background: linear-gradient(to top, rgba(0,80,160,0.1), transparent);
        pointer-events: none;
        z-index: 0;
    }
    .main-header {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 35px 60px;
        width: 100%;
        overflow: hidden;
        background: linear-gradient(135deg, #020c1b 0%, #051428 50%, #020c1b 100%);
        box-shadow: 0 4px 20px rgba(0,196,255,0.12);
        border-bottom: 1px solid rgba(0,196,255,0.12);
        margin-bottom: 25px;
        box-sizing: border-box;
        min-height: 220px;
    }
    .posters-bg {
        position: absolute; top: 0; left: 0;
        width: 100%; height: 100%; pointer-events: none;
    }
    .header-content { position: relative; z-index: 2; text-align: center; width: 100%; }
    .logo img {
        height: 150px;
        filter: drop-shadow(0 0 18px rgba(0,196,255,0.7));
    }
    .logo-text {
        font-size: 28px; font-weight: bold;
        background: linear-gradient(90deg, #00c4ff, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1px;
    }
    .tagline { font-size: 13px; color: #7ecfff; margin-top: 5px; letter-spacing: 0.5px; }
    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #020c1b, #051428);
        color: #ffcc00;
        border: 1px solid rgba(0,196,255,0.4);
        border-radius: 25px;
        font-size: 15px; font-weight: bold;
        padding: 8px 20px; transition: 0.3s;
        letter-spacing: 1px;
        box-shadow: 0 0 10px rgba(0,196,255,0.1);
        width: 100%;
    }
    div[data-testid="stButton"] button:hover {
        background: linear-gradient(135deg, #051428, #0a1f3d);
        color: #00c4ff; border-color: #00c4ff;
        box-shadow: 0 0 16px rgba(0,196,255,0.35);
    }
    textarea, input[type="text"] {
        background-color: #020c1b !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(0,196,255,0.3) !important;
        border-radius: 10px !important;
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 14px !important;
    }
    .accueil-card {
        background: linear-gradient(135deg, #020c1b, #051428);
        border: 1px solid rgba(0,196,255,0.2);
        border-radius: 16px;
        padding: 20px 25px;
        box-shadow: 0 8px 32px rgba(0,196,255,0.08);
        margin-bottom: 15px;
    }
    .accueil-label {
        font-family: 'Segoe UI', sans-serif; font-size: 14px;
        color: #7ecfff; text-align: left;
        margin-bottom: 8px; letter-spacing: 0.5px;
    }
    /* Contact form */
    div[data-testid="stForm"] {
        background: linear-gradient(135deg, #020c1b, #051428);
        border: 1px solid rgba(0,196,255,0.2);
        border-radius: 16px;
        padding: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Header ---
logo_img = f'data:image/png;base64,{logo_base64}'
st.markdown(
    f'<div class="main-header">'
    f'<div class="posters-bg">{posters_html}</div>'
    f'<div class="header-content">'
    f'<div style="display:flex; align-items:center; justify-content:center; gap:60px;">'
    f'<div style="text-align:left;">'
    f'<div class="logo-text">Movie Sentiment AI</div>'
    f'<div class="tagline">Analysez les émotions. Découvrez les films.</div>'
    f'</div>'
    f'<div class="logo"><img src="{logo_img}" alt="Logo"></div>'
    f'</div>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)

# --- Session state ---
if "menu" not in st.session_state:
    st.session_state.menu = " Dashboard"
if "search_mode" not in st.session_state:
    st.session_state.search_mode = False
if "last_query" not in st.session_state:
    st.session_state.last_query = ""

# --- Barre de recherche ---
col_left, col_center, col_right = st.columns([2, 2, 2])
with col_center:
    search_query = st.text_input(
        "",
        placeholder="🔍 Rechercher un film...",
        label_visibility="collapsed",
        key="search_input"
    )

# Active la recherche SEULEMENT si pas en mode retour
if search_query and not st.session_state.get("returning", False):
    st.session_state.search_mode = True
    st.session_state.last_query = search_query

# Reset le flag retour
if st.session_state.get("returning", False):
    st.session_state.returning = False

# --- MODE RECHERCHE ---
if st.session_state.search_mode:
    col1, col2 = st.columns([1, 8])
    with col1:
        if st.button("⬅ Retour"):
            st.session_state.search_mode = False
            st.session_state.last_query = ""
            st.session_state.returning = True  # ← flag retour
            st.session_state.menu = " Dashboard"
            st.rerun()

    st.markdown(
        """
        <div style="text-align:center; margin:20px 0 25px 0;">
            <h3 style="color:#00c4ff; font-size:20px;">🎬 Résultats de recherche</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    results = search_movies(collection, st.session_state.last_query)
    if results:
        show_movies_ai(results)
    else:
        st.warning("❌ Aucun film trouvé.")
    st.stop()
# --- Menu principal ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button(" Dashboard", use_container_width=True):
            st.session_state.menu = " Dashboard"
            st.rerun()
    with btn_col2:
        if st.button(" Notre AI", use_container_width=True):
            st.session_state.menu = " Notre AI"
            st.rerun()

menu = st.session_state.menu

# --- Page Notre AI ---
if menu == " Notre AI":
    st.markdown(
        """
        <div style="max-width:750px; margin:40px auto; text-align:center;">
            <div style="font-family:'Segoe UI',sans-serif; font-size:32px; font-weight:800;
                color:#ffcc00; text-shadow:0 0 16px rgba(255,204,0,0.35);
                letter-spacing:1.5px; margin-bottom:8px;">
                🎬 Analyse de Sentiment
            </div>
            <div style="font-family:'Segoe UI',sans-serif; font-size:15px;
                color:#7ecfff; margin-bottom:20px; letter-spacing:0.5px;">
                Découvrez les films qui correspondent à votre état d'esprit
            </div>
            <div style="width:60px; height:3px;
                background:linear-gradient(90deg,#ffcc00,#00c4ff);
                border-radius:2px; margin:0 auto 28px auto;">
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown(
            '<div class="accueil-card"><div class="accueil-label">💬 Décrivez votre humeur du moment</div></div>',
            unsafe_allow_html=True
        )
        user_text = st.text_area(
            "",
            placeholder="Ex: Je me sens motivé, plein d'énergie et prêt à relever des défis...",
            height=120,
            label_visibility="collapsed"
        )
        analyser = st.button("✨ Analyser mon sentiment", use_container_width=True)

    if analyser:
        if user_text:
            with st.spinner("Analyse en cours..."):
                dominant, user_vector = analyze_user_text(user_text)
                films = get_recommendations(collection, user_vector, top_n=5)

            if len(films) == 0:
                st.warning("⚠️ Aucun film trouvé dans la base.")
            else:
                st.markdown(
                    """
                    <div style="text-align:center; margin:30px 0 15px 0;">
                        <span style="color:#ffcc00; font-size:18px; font-weight:700;
                            text-shadow:0 0 10px rgba(255,204,0,0.3);">
                            🎥 Films recommandés pour vous
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                show_movies_ai(films)
        else:
            st.warning("⚠️ Merci d'entrer votre texte avant d'analyser.")

# --- Page Dashboard ---
elif menu == " Dashboard":
    emotions = ['love', 'happiness', 'sadness', 'enthusiasm', 'hate', 'empty']
    for emo in emotions:
        st.markdown(
            f"""
            <div style="text-align:center; margin:35px 0 18px 0;">
                <h2 style="font-family:'Segoe UI',Arial,sans-serif; font-size:22px;
                    font-weight:700; margin:0; letter-spacing:1px; text-transform:uppercase;">
                    <span style="color:#ffcc00; text-shadow:0 0 12px rgba(255,204,0,0.4);">
                        🎬 Movies that give you
                    </span>
                    <span style="color:#00c4ff; text-shadow:0 0 14px rgba(0,196,255,0.5);">
                        {emo}
                    </span>
                    <span style="color:#ffcc00; text-shadow:0 0 12px rgba(255,204,0,0.4);">
                        vibes
                    </span>
                </h2>
                <div style="width:80px; height:2px;
                    background:linear-gradient(90deg,#ffcc00,#00c4ff);
                    margin:10px auto 0 auto; border-radius:2px;">
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        films = get_recommendations_by_emotion(collection, emo, top_n=10)
        if len(films) == 0:
            st.write(f"❌ Aucun film pour l'émotion {emo}.")
        else:
            show_movie_row(films, emo)

# --- Footer Contact ---
st.markdown(
    """
    <div style="text-align:center; margin-top:60px; margin-bottom:20px;">
        <div style="width:80px; height:2px;
            background:linear-gradient(90deg,#ffcc00,#00c4ff);
            margin:0 auto 25px auto; border-radius:2px;">
        </div>
        <h2 style="color:#ffcc00; font-size:22px; margin-bottom:8px;">📩 Contact Us</h2>
        <p style="color:#7ecfff; font-size:14px;">
            Une question ? Une suggestion ? Envoyez-nous un message 👇
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    with st.form("contact_form"):
        name      = st.text_input("Votre nom")
        email     = st.text_input("Votre email")
        message   = st.text_area("Votre message", height=120)
        submitted = st.form_submit_button("✉️ Envoyer", use_container_width=True)

        if submitted:
            if name and email and message:
                success = send_email(name, email, message)
                if success:
                    st.success("✅ Message envoyé avec succès !")
                else:
                    st.error("❌ Erreur lors de l'envoi. Vérifiez la configuration.")
            else:
                st.error("⚠️ Merci de remplir tous les champs.")
        st.markdown(
    """
    <div style="text-align:center; margin-top:60px; margin-bottom:20px;">
        <div style="width:80px; height:2px;
            background:linear-gradient(90deg,#ffcc00,#00c4ff);
            margin:0 auto 25px auto; border-radius:2px;">
        </div>
        <h2 style="color:#ffcc00; font-size:22px; margin-bottom:8px;">📩 Contact Us</h2>
        <p style="color:#7ecfff; font-size:14px;">
            Une question ? Une suggestion ? Envoyez-nous un message 👇
        </p>
        <a href="mailto:alaouitofa@gmail.com" style="
            color:#00c4ff;
            font-size:15px;
            font-weight:600;
            text-decoration:none;
            background:rgba(0,196,255,0.08);
            border:1px solid rgba(0,196,255,0.3);
            border-radius:20px;
            padding:6px 18px;
            display:inline-block;
            margin-top:8px;
            letter-spacing:0.5px;
        ">✉️ alaouitofa@gmail.com</a>
    </div>
    """,
    unsafe_allow_html=True
)        