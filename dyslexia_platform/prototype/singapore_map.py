"""
Singapore Map Journey & Virtual Robot Assistant
================================================
- Real Singapore map with landmarks as module stops
- Robot assistant that guides the child at each module
"""

# =============================================================================
# SINGAPORE LANDMARKS (4 per level = 20 total stops)
# =============================================================================
SINGAPORE_LANDMARKS = {
    1: [
        {"name": "Merlion Park", "emoji": "🦁", "lat": 1.2868, "lng": 103.8545},
        {"name": "Marina Bay Sands", "emoji": "🏨", "lat": 1.2834, "lng": 103.8607},
        {"name": "Gardens by the Bay", "emoji": "🌳", "lat": 1.2816, "lng": 103.8636},
        {"name": "Singapore Flyer", "emoji": "🎡", "lat": 1.2893, "lng": 103.8631},
    ],
    2: [
        {"name": "Sentosa Island", "emoji": "🏝️", "lat": 1.2494, "lng": 103.8303},
        {"name": "Universal Studios", "emoji": "🎢", "lat": 1.2540, "lng": 103.8238},
        {"name": "S.E.A. Aquarium", "emoji": "🐠", "lat": 1.2581, "lng": 103.8194},
        {"name": "Fort Siloso", "emoji": "🏰", "lat": 1.2600, "lng": 103.8100},
    ],
    3: [
        {"name": "Chinatown", "emoji": "🏮", "lat": 1.2833, "lng": 103.8443},
        {"name": "Little India", "emoji": "🪷", "lat": 1.3066, "lng": 103.8518},
        {"name": "Kampong Glam", "emoji": "🕌", "lat": 1.3025, "lng": 103.8594},
        {"name": "Clarke Quay", "emoji": "🌉", "lat": 1.2906, "lng": 103.8464},
    ],
    4: [
        {"name": "Botanic Gardens", "emoji": "🌺", "lat": 1.3138, "lng": 103.8159},
        {"name": "Orchard Road", "emoji": "🛍️", "lat": 1.3048, "lng": 103.8318},
        {"name": "National Museum", "emoji": "🏛️", "lat": 1.2966, "lng": 103.8485},
        {"name": "Esplanade", "emoji": "🎭", "lat": 1.2899, "lng": 103.8557},
    ],
    5: [
        {"name": "Jewel Changi", "emoji": "💎", "lat": 1.3604, "lng": 103.9894},
        {"name": "East Coast Park", "emoji": "🏖️", "lat": 1.3010, "lng": 103.9125},
        {"name": "MacRitchie Reservoir", "emoji": "🌿", "lat": 1.3430, "lng": 103.8340},
        {"name": "Mount Faber", "emoji": "⛰️", "lat": 1.2714, "lng": 103.8195},
    ],
}

# =============================================================================
# ROBOT ASSISTANT MESSAGES
# =============================================================================
ROBOT_NAME = "Robo"
ROBOT_EMOJI = "🤖"

ROBOT_MODULE_INTRO = {
    "L1M1": {
        "greeting": "Hey there, explorer! 🌟",
        "message": "I'm **Robo**, your learning buddy! We're starting at **Merlion Park** 🦁 — just like the Merlion is made of letters, we're going to learn all about letters today!",
        "tip": "Look carefully at each letter. Some letters look alike but face different ways!",
    },
    "L1M2": {
        "greeting": "Welcome back, superstar! ⭐",
        "message": "We've arrived at **Marina Bay Sands** 🏨! Did you know each letter has its own special sound? Let's discover them!",
        "tip": "Try saying each sound out loud — your mouth and lips will help you remember!",
    },
    "L1M3": {
        "greeting": "You're doing amazing! 🚀",
        "message": "Look at us at **Gardens by the Bay** 🌳! Just like flowers connect to roots, letters connect to sounds. Let's map them together!",
        "tip": "When you see a letter, try to hear its sound in your head!",
    },
    "L1M4": {
        "greeting": "Almost there, champion! 🏆",
        "message": "We made it to the **Singapore Flyer** 🎡! From up high, we can see how letters come together to make words. Let's read some CVC words!",
        "tip": "Sound out each letter one by one, then blend them together fast!",
    },
    "L2M1": {
        "greeting": "New adventure begins! 🏝️",
        "message": "Welcome to **Sentosa Island** 🏝️! Two letters can team up to make new sounds — like 'sh', 'ch', and 'th'. Let's explore blends!",
        "tip": "Listen for the two sounds smooshing together!",
    },
    "L2M2": {
        "greeting": "Keep going, rockstar! 🎸",
        "message": "We're at **Universal Studios** 🎢! Some words are used SO often, we need to know them by sight. Let's learn these superstar words!",
        "tip": "These words are tricky — you just have to remember what they look like!",
    },
    "L2M3": {
        "greeting": "Fantastic progress! 🐠",
        "message": "Diving into the **S.E.A. Aquarium** 🐠! Just like fish swim in groups, words swim together in sentences. Let's read some!",
        "tip": "Point to each word as you read. Take your time!",
    },
    "L2M4": {
        "greeting": "You're a hero! 🏰",
        "message": "Exploring **Fort Siloso** 🏰! Words can rhyme — they sound the same at the end. Like 'cat' and 'hat'. Let's find rhyming patterns!",
        "tip": "Listen to the ending sounds — if they match, they rhyme!",
    },
    "L3M1": {
        "greeting": "Level up! 🏮",
        "message": "Welcome to **Chinatown** 🏮! Just like Chinese characters have parts, big words have syllables. Let's break them apart!",
        "tip": "Clap for each part of the word — each clap is one syllable!",
    },
    "L3M2": {
        "greeting": "Smooth sailing! 🪷",
        "message": "Visiting **Little India** 🪷! Reading fluently means reading smoothly, like music. Let's practice flowing through words!",
        "tip": "Don't rush! Read like you're talking to a friend.",
    },
    "L3M3": {
        "greeting": "Pattern master! 🕌",
        "message": "At **Kampong Glam** 🕌! The beautiful patterns here remind us that spelling has patterns too. Let's crack the code!",
        "tip": "Many words follow the same spelling rules. Once you know the rule, you know many words!",
    },
    "L3M4": {
        "greeting": "Reading time! 🌉",
        "message": "Relaxing at **Clarke Quay** 🌉! The river tells a story as it flows — let's read paragraphs that tell stories too!",
        "tip": "After reading, ask yourself: What was this about? What happened?",
    },
    "L4M1": {
        "greeting": "Advanced explorer! 🌺",
        "message": "At the **Botanic Gardens** 🌺! Just like rare flowers, some letter combinations are tricky. Let's master them!",
        "tip": "Some letters are silent — they're there but don't make a sound!",
    },
    "L4M2": {
        "greeting": "Deep thinker! 🛍️",
        "message": "Strolling down **Orchard Road** 🛍️! Reading isn't just seeing words — it's understanding what they mean together!",
        "tip": "Ask yourself: Why did this happen? How does the character feel?",
    },
    "L4M3": {
        "greeting": "Writer in training! 🏛️",
        "message": "At the **National Museum** 🏛️! Museums tell stories — now it's YOUR turn to write stories!",
        "tip": "Start with: Who? What? Where? Then build your sentence around that!",
    },
    "L4M4": {
        "greeting": "Word wizard! 🎭",
        "message": "At the **Esplanade** 🎭! Actors use many words — let's build YOUR vocabulary with prefixes and suffixes!",
        "tip": "Break big words into parts: prefix + root + suffix. Each part has a meaning!",
    },
    "L5M1": {
        "greeting": "Independent reader! 💎",
        "message": "At **Jewel Changi** 💎! Like this sparkling place, your reading skills are shining! Time to read on your own!",
        "tip": "Trust yourself — you know more than you think!",
    },
    "L5M2": {
        "greeting": "Critical thinker! 🏖️",
        "message": "At **East Coast Park** 🏖️! Look at the big picture — just like the ocean view. What does the text REALLY mean?",
        "tip": "Think about what the author didn't say. Read between the lines!",
    },
    "L5M3": {
        "greeting": "Creative genius! 🌿",
        "message": "At **MacRitchie Reservoir** 🌿! Nature inspires creativity — let your imagination flow like the water!",
        "tip": "There's no wrong answer in creative writing. Just be YOU!",
    },
    "L5M4": {
        "greeting": "Almost at the summit! ⛰️",
        "message": "Climbing **Mount Faber** ⛰️! The final skill: catching your own mistakes. You're becoming your own teacher!",
        "tip": "Read your work slowly out loud. Your ears will catch what your eyes missed!",
    },
}


def get_robot_intro(level: int, module_index: int) -> dict:
    """Get robot assistant intro for a specific module."""
    module_id = f"L{level}M{module_index + 1}"
    default = {
        "greeting": f"Let's go, learner! {ROBOT_EMOJI}",
        "message": f"Starting a new module! I'm **{ROBOT_NAME}**, and I'll be here to help you every step of the way!",
        "tip": "Take your time and do your best!",
    }
    return ROBOT_MODULE_INTRO.get(module_id, default)


def get_landmark(level: int, module_index: int) -> dict:
    """Get Singapore landmark for current progress."""
    landmarks = SINGAPORE_LANDMARKS.get(level, SINGAPORE_LANDMARKS[1])
    if module_index < len(landmarks):
        return landmarks[module_index]
    return landmarks[0]


def get_map_html(level: int, current_module_index: int, module_progress: dict) -> str:
    """Generate HTML for Singapore map with route and progress markers."""
    landmarks = SINGAPORE_LANDMARKS.get(level, SINGAPORE_LANDMARKS[1])

    # Center map on Singapore
    center_lat = 1.3000
    center_lng = 103.8500

    # Build markers
    markers_js = ""
    polyline_points = []

    for i, landmark in enumerate(landmarks):
        lat, lng = landmark["lat"], landmark["lng"]
        polyline_points.append(f"[{lat}, {lng}]")

        # Determine marker color
        status = module_progress.get(i, "locked")
        if i == current_module_index:
            color = "#1976d2"  # current - blue
        elif status == "passed":
            color = "#28a745"  # completed - green
        else:
            color = "#9e9e9e"  # locked - gray

        popup_text = f"{landmark['emoji']} {landmark['name']} - Module {i+1}"

        markers_js += f"""
        L.marker([{lat}, {lng}], {{
            icon: L.divIcon({{
                html: '<div style="background:{color};color:white;border-radius:50%;width:40px;height:40px;display:flex;align-items:center;justify-content:center;font-size:20px;border:3px solid white;box-shadow:0 2px 8px rgba(0,0,0,0.3);">{landmark["emoji"]}</div>',
                iconSize: [40, 40],
                iconAnchor: [20, 20],
                className: ''
            }})
        }}).addTo(map).bindPopup("{popup_text}");
        """

    # Build polyline (route)
    polyline_js = f"L.polyline([{','.join(polyline_points)}], {{color: '#667eea', weight: 4, dashArray: '10 5', opacity: 0.6}}).addTo(map);"

    # Highlight completed route
    completed_points = [f"[{landmarks[i]['lat']}, {landmarks[i]['lng']}]"
                        for i in range(current_module_index + 1)]
    if len(completed_points) > 1:
        completed_line_js = f"L.polyline([{','.join(completed_points)}], {{color: '#28a745', weight: 5}}).addTo(map);"
    else:
        completed_line_js = ""

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        body {{ margin: 0; padding: 0; }}
        #map {{ height: 300px; width: 100%; border-radius: 12px; }}
        .traveler {{
            animation: pulse 1.5s ease-in-out infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.2); }}
        }}
        .route-animated {{
            stroke-dasharray: 12;
            animation: dash 1.5s linear infinite;
        }}
        @keyframes dash {{
            to {{ stroke-dashoffset: -24; }}
        }}
    </style>
</head>
<body>
    <div id="map"></div>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        var map = L.map('map').setView([{center_lat}, {center_lng}], 12);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap',
            maxZoom: 18
        }}).addTo(map);
        
        // Dashed route (full path)
        {polyline_js}
        
        // Green completed route
        {completed_line_js}
        
        // Markers
        {markers_js}
        
        // Animated traveling robot at current position
        var currentLat = {landmarks[current_module_index]["lat"]};
        var currentLng = {landmarks[current_module_index]["lng"]};
        var traveler = L.marker([currentLat, currentLng], {{
            icon: L.divIcon({{
                html: '<div class="traveler" style="background:#ff5722;color:white;border-radius:50%;width:28px;height:28px;display:flex;align-items:center;justify-content:center;font-size:16px;border:2px solid white;box-shadow:0 0 12px rgba(255,87,34,0.6);">🤖</div>',
                iconSize: [28, 28],
                iconAnchor: [14, 14],
                className: ''
            }}),
            zIndexOffset: 1000
        }}).addTo(map);
        
        // Animate travel from previous to current if module > 0
        var moduleIndex = {current_module_index};
        if (moduleIndex > 0) {{
            var points = [{','.join(polyline_points)}];
            var prevPoint = points[moduleIndex - 1];
            var currPoint = points[moduleIndex];
            
            // Animate the robot moving
            var startLat = prevPoint[0], startLng = prevPoint[1];
            var endLat = currPoint[0], endLng = currPoint[1];
            var steps = 60;
            var step = 0;
            
            traveler.setLatLng([startLat, startLng]);
            
            function animateTravel() {{
                step++;
                var progress = step / steps;
                // Ease-in-out
                progress = progress < 0.5 ? 2*progress*progress : 1-Math.pow(-2*progress+2,2)/2;
                var lat = startLat + (endLat - startLat) * progress;
                var lng = startLng + (endLng - startLng) * progress;
                traveler.setLatLng([lat, lng]);
                if (step < steps) {{
                    requestAnimationFrame(animateTravel);
                }}
            }}
            
            // Start animation after a short delay
            setTimeout(animateTravel, 500);
        }}
        
        // Fit map to show all landmarks
        var bounds = L.latLngBounds([{','.join(polyline_points)}]);
        map.fitBounds(bounds, {{padding: [30, 30]}});
    </script>
</body>
</html>"""
    return html


def get_robot_html(greeting: str, message: str, tip: str) -> str:
    """Generate HTML for the robot assistant popup."""
    return f"""
    <div style="
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #64b5f6;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
        box-shadow: 0 6px 20px rgba(100, 181, 246, 0.2);
    ">
        <div style="
            position: absolute;
            top: -20px;
            left: 20px;
            background: #1976d2;
            color: white;
            border-radius: 50%;
            width: 44px;
            height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        ">🤖</div>
        <div style="margin-left: 50px;">
            <p style="font-weight:600;color:#1565c0;margin:0;font-size:1.1rem;">{greeting}</p>
            <p style="margin:0.5rem 0;color:#333;">{message}</p>
            <div style="
                background: rgba(255,255,255,0.7);
                border-radius: 10px;
                padding: 0.6rem 1rem;
                margin-top: 0.5rem;
                border-left: 4px solid #ffc107;
            ">
                <strong>💡 Tip:</strong> {tip}
            </div>
        </div>
    </div>
    """


def get_floating_robot_html(message: str = "I'm here to help! 🌟") -> str:
    """Generate HTML for a floating robot assistant at bottom-right corner."""
    return f"""
    <div id="floating-robot" style="
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9999;
        display: flex;
        align-items: flex-end;
        gap: 10px;
        animation: robotBounce 2s ease-in-out infinite;
    ">
        <div style="
            background: white;
            border: 2px solid #64b5f6;
            border-radius: 16px 16px 4px 16px;
            padding: 10px 16px;
            max-width: 220px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            font-family: 'Lexend', sans-serif;
            font-size: 0.85rem;
            color: #333;
        ">{message}</div>
        <div style="
            background: linear-gradient(135deg, #1976d2, #1565c0);
            border-radius: 50%;
            width: 56px;
            height: 56px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            box-shadow: 0 4px 15px rgba(25, 118, 210, 0.4);
            cursor: pointer;
            border: 3px solid white;
        ">🤖</div>
    </div>
    <style>
        @keyframes robotBounce {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-5px); }}
        }}
    </style>
    """


def get_robot_congrats_html(landmark_name: str, landmark_emoji: str, next_landmark: str = None) -> str:
    """Generate HTML for robot congratulating on passing exam and reaching destination."""
    if next_landmark:
        next_text = f"Next stop: <strong>{next_landmark}</strong>! Let's keep exploring! 🚀"
    else:
        next_text = "You've completed the entire journey! You're a <strong>reading champion</strong>! 🏆👑"

    return f"""
    <div style="
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border: 3px solid #4caf50;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        position: relative;
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.25);
        text-align: center;
    ">
        <div style="font-size: 48px; margin-bottom: 0.5rem;">🤖🎉</div>
        <h3 style="color: #2e7d32; margin: 0.5rem 0;">
            Congratulations! You reached {landmark_emoji} {landmark_name}!
        </h3>
        <p style="color: #333; font-size: 1rem; margin: 0.5rem 0;">
            Amazing work, explorer! You passed the exam and moved forward on your Singapore adventure!
        </p>
        <p style="color: #555; margin-top: 0.5rem;">{next_text}</p>
    </div>
    """
