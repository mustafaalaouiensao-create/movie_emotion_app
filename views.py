import streamlit as st
import streamlit.components.v1 as components

def show_movie_row(films, emotion):

    slides_html = ""
    for film in films:
        title    = str(film.get('title', '')).replace("'", " ").replace('"', ' ')
        year     = str(film.get('year', ''))
        synopsis = str(film.get('synopsis', 'Pas de synopsis')).replace("'", " ").replace('"', ' ')
        genres   = ', '.join(film.get('genres', []))
        duration = str(film.get('duration', 'Inconnue'))
        rating   = str(film.get('rating', 0))
        poster   = str(film.get('poster_url', ''))
        sim      = str(round(float(film.get('similarity', 0)), 2))

        slides_html += f"""
        <div class="swiper-slide" onclick="showDetails('{title}','{year}','{synopsis}','{genres}','{duration}','{rating}')">
            <img src="{poster}" onerror="this.src=''" 
                 style="width:160px; height:240px; object-fit:cover; border-radius:10px; cursor:pointer;"/>
            <h4 style="margin:8px 0; font-size:14px; font-weight:bold; color:#ffcc00;">
                {title}
            </h4>
            <p style="font-size:11px; color:#aaa;">({year}) | ⭐ {rating}</p>
            <p style="font-size:11px; color:#7ecfff;">{genres}</p>
        </div>
        """

    full_html = """
    <html>
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css"/>
        <style>
            body { margin:0; background:transparent; font-family:'Segoe UI',sans-serif; }
            .swiper { width:100%; padding:10px 0 40px 0; }
            .swiper-slide {
                background: linear-gradient(135deg, #0d1b3e, #0a0f1e);
                border: 1px solid rgba(0,196,255,0.15);
                border-radius: 12px;
                padding: 12px;
                text-align: center;
                color: white;
                cursor: pointer;
                transition: 0.3s;
            }
            .swiper-slide:hover {
                border-color: #00c4ff;
                box-shadow: 0 0 16px rgba(0,196,255,0.3);
                transform: translateY(-4px);
            }
            .swiper-button-next,
            .swiper-button-prev { color: #ffcc00; }
            #filmModal {
                display: none;
                position: fixed;
                top: 15%;
                left: 50%;
                transform: translateX(-50%);
                background: linear-gradient(135deg, #0d1b3e, #0a0f1e);
                border: 1px solid rgba(0,196,255,0.3);
                color: white;
                padding: 25px;
                border-radius: 16px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.6);
                z-index: 9999;
                max-width: 420px;
                width: 90%;
            }
            #modalTitle { color:#ffcc00; font-size:20px; margin-bottom:10px; }
            .modal-field { color:#7ecfff; font-size:13px; margin:6px 0; }
            .close-btn {
                margin-top:15px; padding:8px 20px;
                border:none; border-radius:20px;
                background: linear-gradient(135deg, #ffcc00, #f59e0b);
                color:#0a0f1e; font-weight:800;
                cursor:pointer; font-size:14px;
            }
        </style>
    </head>
    <body>
        <div class="swiper mySwiper">
            <div class="swiper-wrapper">
                """ + slides_html + """
            </div>
            <div class="swiper-button-next"></div>
            <div class="swiper-button-prev"></div>
        </div>

        <div id="filmModal">
            <div id="modalTitle"></div>
            <p class="modal-field" id="modalYear"></p>
            <p class="modal-field" id="modalSynopsis"></p>
            <p class="modal-field" id="modalGenres"></p>
            <p class="modal-field" id="modalDuration"></p>
            <p class="modal-field" id="modalRating"></p>
            <button class="close-btn" onclick="document.getElementById('filmModal').style.display='none'">
                ✕ Fermer
            </button>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
        <script>
            new Swiper('.mySwiper', {
                loop: true,
                slidesPerView: 5,
                spaceBetween: 15,
                autoplay: { delay: 2500, disableOnInteraction: false },
                navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' },
                breakpoints: {
                    320:  { slidesPerView: 2 },
                    768:  { slidesPerView: 3 },
                    1024: { slidesPerView: 5 }
                }
            });

            function showDetails(title, year, synopsis, genres, duration, rating) {
                document.getElementById('modalTitle').innerText = title;
                document.getElementById('modalYear').innerText = "📅 Année : " + year;
                document.getElementById('modalSynopsis').innerText = "📝 " + synopsis;
                document.getElementById('modalGenres').innerText = "🎭 Genres : " + genres;
                document.getElementById('modalDuration').innerText = "⏱ Durée : " + duration + " min";
                document.getElementById('modalRating').innerText = "⭐ Note : " + rating;
                document.getElementById('filmModal').style.display = 'block';
            }
        </script>
    </body>
    </html>
    """

    # Titre émotion
    st.markdown(
        f"""
        <div style="text-align:center; margin:35px 0 18px 0;">
            <h2 style="font-family:'Segoe UI',Arial,sans-serif; font-size:22px;
                font-weight:700; margin:0; letter-spacing:1px; text-transform:uppercase;">
                <span style="color:#ffcc00; text-shadow:0 0 12px rgba(255,204,0,0.4);">
                    🎬 Movies that give you
                </span>
                <span style="color:#00c4ff; text-shadow:0 0 14px rgba(0,196,255,0.5);">
                    {emotion}
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

    components.html(full_html, height=420, scrolling=False)
def show_movies_ai(films):
    import random
    uid = str(random.randint(10000, 99999))

    modal_html = ""
    cards_html = ""

    for rank, film in enumerate(films, start=1):
        title        = str(film.get('title', '')).replace("'", " ").replace('"', ' ')
        year         = str(film.get('year', ''))
        synopsis     = str(film.get('synopsis', 'Pas de synopsis')).replace("'", " ").replace('"', ' ')
        genres       = ', '.join(film.get('genres', []))
        duration_raw = film.get('duration', '')
        duration     = str(duration_raw) if duration_raw else 'N/A'
        rating       = str(film.get('rating', 0))
        poster       = str(film.get('poster_url', ''))
        sim          = str(round(float(film.get('similarity', 0)), 2))
        langue       = str(film.get('langue', film.get('language', film.get('original_language', 'N/A'))))
        pays         = str(film.get('pays', film.get('country', film.get('production_countries', 'N/A'))))
        budget       = str(film.get('budget', 'N/A'))
        recette      = str(film.get('revenue', film.get('recette', 'N/A')))
        directeur    = str(film.get('director', film.get('directeur', 'N/A')))
        acteurs_raw  = film.get('actors', film.get('acteurs', []))
        acteurs      = ', '.join(acteurs_raw) if isinstance(acteurs_raw, list) else str(acteurs_raw)

        if rank == 1:
            medal = "🥇"; border_color = "rgba(255,204,0,0.7)"; rank_color = "#ffcc00"
        elif rank == 2:
            medal = "🥈"; border_color = "rgba(192,192,192,0.7)"; rank_color = "#c0c0c0"
        elif rank == 3:
            medal = "🥉"; border_color = "rgba(205,127,50,0.7)"; rank_color = "#cd7f32"
        else:
            medal = f"#{rank}"; border_color = "rgba(0,196,255,0.2)"; rank_color = "#7ecfff"

        duration_badge = f"⏱ {duration} min" if duration != "N/A" else "⏱ N/A"
        film_id = f"film_{uid}_{rank}"

        cards_html += f"""
        <div style="display:flex; gap:15px; align-items:flex-start; margin-bottom:15px;">
            <div style="min-width:50px; text-align:center; font-size:26px; font-weight:900;
                color:{rank_color}; text-shadow:0 0 12px {rank_color}; padding-top:15px;">
                {medal}
            </div>
            <div style="background:linear-gradient(135deg,#020c1b,#051428);
                border:1px solid {border_color}; border-radius:14px;
                padding:18px 22px; flex:1;
                box-shadow:0 4px 20px rgba(0,0,0,0.4);
                display:flex; gap:20px; align-items:flex-start;">
                <img src="{poster}" onerror="this.style.display='none'"
                     onclick="document.getElementById('{film_id}').style.display='flex'"
                     style="width:110px; height:160px; object-fit:cover; border-radius:10px;
                     flex-shrink:0; box-shadow:0 4px 12px rgba(0,0,0,0.5);
                     cursor:pointer; transition:0.3s;"
                     onmouseover="this.style.transform='scale(1.05)'"
                     onmouseout="this.style.transform='scale(1)'"/>
                <div style="flex:1;">
                    <div style="font-size:17px; font-weight:800; color:#ffcc00;
                        text-shadow:0 0 10px rgba(255,204,0,0.3); margin-bottom:10px;">
                        {title}
                        <span style="color:#aaa; font-size:13px; font-weight:400;">({year})</span>
                    </div>
                    <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:10px;">
                        <span style="background:rgba(0,196,255,0.1); border:1px solid rgba(0,196,255,0.3);
                            border-radius:20px; padding:3px 12px; font-size:12px; color:#7ecfff;">🎭 {genres}</span>
                        <span style="background:rgba(255,204,0,0.1); border:1px solid rgba(255,204,0,0.3);
                            border-radius:20px; padding:3px 12px; font-size:12px; color:#ffcc00;">⭐ {rating}</span>
                        <span style="background:rgba(0,196,255,0.1); border:1px solid rgba(0,196,255,0.2);
                            border-radius:20px; padding:3px 12px; font-size:12px; color:#7ecfff;">{duration_badge}</span>
                        <span style="background:rgba(0,255,100,0.1); border:1px solid rgba(0,255,100,0.2);
                            border-radius:20px; padding:3px 12px; font-size:12px; color:#00ff88;">🎯 {sim}</span>
                    </div>
                    <div style="font-size:13px; color:#94a3b8; line-height:1.6; font-style:italic;">
                        {synopsis[:200]}...
                    </div>
                </div>
            </div>
        </div>

        <div id="{film_id}" style="display:none; position:fixed; top:0; left:0;
            width:100%; height:100%; background:rgba(0,0,0,0.88);
            z-index:9999; justify-content:center; align-items:center;"
            onclick="if(event.target===this)this.style.display='none'">
            <div style="background:linear-gradient(135deg,#020c1b,#051428);
                border:1px solid rgba(0,196,255,0.35); border-radius:24px;
                padding:35px; max-width:900px; width:95%;
                box-shadow:0 20px 60px rgba(0,0,0,0.9); position:relative;
                max-height:90vh; overflow-y:auto;">
                <button onclick="document.getElementById('{film_id}').style.display='none'"
                    style="position:absolute; top:18px; right:18px;
                    background:rgba(255,80,80,0.2); border:1px solid rgba(255,80,80,0.4);
                    color:#ff5050; border-radius:50%; width:36px; height:36px;
                    cursor:pointer; font-size:18px; font-weight:bold; line-height:36px;">✕</button>
                <div style="display:flex; gap:30px; align-items:flex-start;">
                    <img src="{poster}" onerror="this.style.display='none'"
                         style="width:200px; height:300px; object-fit:cover;
                         border-radius:14px; flex-shrink:0;
                         box-shadow:0 10px 30px rgba(0,0,0,0.7);"/>
                    <div style="flex:1;">
                        <div style="font-size:24px; font-weight:900; color:#ffcc00;
                            text-shadow:0 0 14px rgba(255,204,0,0.4); margin-bottom:8px;">
                            {title}
                        </div>
                        <div style="color:#7ecfff; font-size:14px; margin-bottom:18px;">
                            {year} • {genres}
                        </div>
                        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:18px;">
                            <span style="background:rgba(255,204,0,0.1); border:1px solid rgba(255,204,0,0.3);
                                border-radius:20px; padding:5px 16px; font-size:13px; color:#ffcc00;">⭐ {rating}</span>
                            <span style="background:rgba(0,196,255,0.1); border:1px solid rgba(0,196,255,0.2);
                                border-radius:20px; padding:5px 16px; font-size:13px; color:#7ecfff;">{duration_badge}</span>
                            <span style="background:rgba(0,255,100,0.1); border:1px solid rgba(0,255,100,0.2);
                                border-radius:20px; padding:5px 16px; font-size:13px; color:#00ff88;">🎯 {sim}</span>
                        </div>
                        <div style="font-size:13px; color:#94a3b8; line-height:2.0;">
                            <div style="margin-bottom:5px;">
                                <span style="color:#7ecfff; font-weight:600;">🎬 Réalisateur :</span> {directeur}
                            </div>
                            <div style="margin-bottom:5px;">
                                <span style="color:#7ecfff; font-weight:600;">🎭 Acteurs :</span> {acteurs if acteurs else 'N/A'}
                            </div>
                            <div style="margin-bottom:5px;">
                                <span style="color:#7ecfff; font-weight:600;">🌍 Langue :</span> {langue}
                            </div>
                            <div style="margin-bottom:5px;">
                                <span style="color:#7ecfff; font-weight:600;">🗺 Pays :</span> {pays}
                            </div>
                            <div style="margin-bottom:5px;">
                                <span style="color:#7ecfff; font-weight:600;">💰 Budget :</span> {budget}
                            </div>
                            <div style="margin-bottom:5px;">
                                <span style="color:#7ecfff; font-weight:600;">💵 Recette :</span> {recette}
                            </div>
                        </div>
                    </div>
                </div>
                <div style="margin-top:25px; padding-top:20px;
                    border-top:1px solid rgba(0,196,255,0.15);">
                    <div style="color:#7ecfff; font-size:13px; font-weight:600;
                        margin-bottom:10px; letter-spacing:0.5px;">📝 Synopsis</div>
                    <div style="font-size:14px; color:#94a3b8; line-height:1.8; font-style:italic;">
                        {synopsis}
                    </div>
                </div>
            </div>
        </div>
        """

    full_html = f"""
    <html><head>
    <style>
        body {{ margin:0; background:transparent; font-family:'Segoe UI',sans-serif; }}
        ::-webkit-scrollbar {{ width:6px; }}
        ::-webkit-scrollbar-track {{ background:transparent; }}
        ::-webkit-scrollbar-thumb {{ background:#00c4ff44; border-radius:3px; }}
    </style>
    </head><body>
        {cards_html}
    </body></html>
    """

    components.html(full_html, height=len(films) * 220, scrolling=True)