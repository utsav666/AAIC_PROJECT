"""
Video & Module Bank
====================
Maps YouTube videos and module definitions to each dyslexia level.
Each level has 4 modules, each module has a video + description.
"""

# =============================================================================
# LEVEL → MODULE → VIDEO MAPPING
# =============================================================================

LEARNING_MODULES = {
    1: {
        "name": "Level 1 - Foundation",
        "description": "Building basic letter and sound awareness",
        "modules": [
            {
                "id": "L1M1",
                "name": "Letter Recognition",
                "description": "Learning to identify and distinguish letters correctly (especially b/d, p/q)",
                "video_url": "https://www.youtube.com/watch?v=36IBDpTRVNE",
                "video_title": "Learn the Alphabet A-Z | Jack Hartmann",
                "skills": ["identify uppercase letters", "identify lowercase letters", "distinguish similar letters"],
                "exam_focus": "Correctly identifying letters, especially commonly confused pairs",
            },
            {
                "id": "L1M2",
                "name": "Basic Phonics",
                "description": "Learning the sounds each letter makes",
                "video_url": "https://www.youtube.com/watch?v=BELlZKpi1Zs",
                "video_title": "Phonics - Learn to Read | Alphablocks",
                "skills": ["letter-sound correspondence", "initial sounds", "ending sounds"],
                "exam_focus": "Matching letters to their sounds and identifying sounds in words",
            },
            {
                "id": "L1M3",
                "name": "Letter-Sound Mapping",
                "description": "Connecting written letters to spoken sounds",
                "video_url": "https://www.youtube.com/watch?v=jvAYUvQUrGo",
                "video_title": "Letter Sounds A-Z | Pinkfong",
                "skills": ["sound blending", "sound segmenting", "letter-sound pairs"],
                "exam_focus": "Blending individual sounds to form simple words",
            },
            {
                "id": "L1M4",
                "name": "Simple CVC Words",
                "description": "Reading and spelling 3-letter consonant-vowel-consonant words (cat, dog, pen)",
                "video_url": "https://www.youtube.com/watch?v=SAvTalKzSao",
                "video_title": "CVC Words for Kids | Rock 'N Learn",
                "skills": ["read CVC words", "spell CVC words", "rhyming CVC words"],
                "exam_focus": "Reading and spelling simple 3-letter words correctly",
            },
        ],
    },
    2: {
        "name": "Level 2 - Building Blocks",
        "description": "Developing word patterns and sight word recognition",
        "modules": [
            {
                "id": "L2M1",
                "name": "Blends & Digraphs",
                "description": "Learning consonant blends (bl, cr, st) and digraphs (sh, ch, th)",
                "video_url": "https://www.youtube.com/watch?v=DEHBrmZxAf8",
                "video_title": "Consonant Blends | Jack Hartmann",
                "skills": ["identify blends", "read blend words", "digraph sounds"],
                "exam_focus": "Recognizing and reading words with blends and digraphs",
            },
            {
                "id": "L2M2",
                "name": "Sight Words Set 1",
                "description": "Memorizing high-frequency words that don't follow phonics rules",
                "video_url": "https://www.youtube.com/watch?v=ezFRg11GdAI",
                "video_title": "Sight Words | Scratch Garden",
                "skills": ["recognize sight words", "read sight words in context", "spell sight words"],
                "exam_focus": "Reading and spelling common sight words quickly",
            },
            {
                "id": "L2M3",
                "name": "Short Sentences",
                "description": "Reading and understanding simple sentences",
                "video_url": "https://www.youtube.com/watch?v=d0FMsb5vXOI",
                "video_title": "Reading Simple Sentences | Kids Academy",
                "skills": ["sentence reading", "word spacing", "basic punctuation"],
                "exam_focus": "Reading short sentences fluently and understanding meaning",
            },
            {
                "id": "L2M4",
                "name": "Rhyming Patterns",
                "description": "Recognizing word families and rhyming patterns (-at, -ig, -op)",
                "video_url": "https://www.youtube.com/watch?v=FnUFrGNfEKM",
                "video_title": "Rhyming Words | Scratch Garden",
                "skills": ["identify rhymes", "word families", "pattern recognition"],
                "exam_focus": "Identifying and generating rhyming words in word families",
            },
        ],
    },
    3: {
        "name": "Level 3 - Developing",
        "description": "Building fluency and tackling longer words",
        "modules": [
            {
                "id": "L3M1",
                "name": "Multi-Syllable Words",
                "description": "Breaking longer words into syllables for easier reading",
                "video_url": "https://www.youtube.com/watch?v=MlM1oOiwBbI",
                "video_title": "Syllables | Scratch Garden",
                "skills": ["syllable counting", "syllable breaking", "reading multi-syllable words"],
                "exam_focus": "Breaking words into syllables and reading them correctly",
            },
            {
                "id": "L3M2",
                "name": "Reading Fluency",
                "description": "Reading smoothly with appropriate speed and expression",
                "video_url": "https://www.youtube.com/watch?v=s3Eh4k3Gdhs",
                "video_title": "Reading Fluency | Khan Academy Kids",
                "skills": ["reading speed", "expression", "self-correction"],
                "exam_focus": "Reading passages with understanding and appropriate pacing",
            },
            {
                "id": "L3M3",
                "name": "Spelling Patterns",
                "description": "Learning common spelling rules and patterns (magic-e, double consonants)",
                "video_url": "https://www.youtube.com/watch?v=OufL5jSIcgE",
                "video_title": "Spelling Rules | English with Lucy",
                "skills": ["spelling rules", "pattern application", "word building"],
                "exam_focus": "Applying spelling patterns to spell words correctly",
            },
            {
                "id": "L3M4",
                "name": "Paragraph Reading",
                "description": "Reading and understanding short paragraphs",
                "video_url": "https://www.youtube.com/watch?v=LvUov5_2Afs",
                "video_title": "Reading Comprehension | Crash Course Kids",
                "skills": ["paragraph comprehension", "main idea", "details"],
                "exam_focus": "Reading a paragraph and answering questions about it",
            },
        ],
    },
    4: {
        "name": "Level 4 - Advancing",
        "description": "Strengthening comprehension and written expression",
        "modules": [
            {
                "id": "L4M1",
                "name": "Complex Phonics",
                "description": "Advanced phonics patterns (diphthongs, r-controlled vowels, silent letters)",
                "video_url": "https://www.youtube.com/watch?v=GfRU7sZp-64",
                "video_title": "Advanced Phonics | English4Kids",
                "skills": ["diphthongs", "r-controlled vowels", "silent letters"],
                "exam_focus": "Reading and spelling words with complex phonics patterns",
            },
            {
                "id": "L4M2",
                "name": "Comprehension Skills",
                "description": "Understanding meaning, making inferences, finding main ideas",
                "video_url": "https://www.youtube.com/watch?v=1kq9svh-cGE",
                "video_title": "Reading Comprehension | Crash Course Kids",
                "skills": ["inference", "main idea", "supporting details", "vocabulary in context"],
                "exam_focus": "Reading a passage and demonstrating deeper understanding",
            },
            {
                "id": "L4M3",
                "name": "Writing Support",
                "description": "Structuring sentences and short paragraphs",
                "video_url": "https://www.youtube.com/watch?v=bMQ-aCP_-hA",
                "video_title": "Sentence Writing | Khan Academy",
                "skills": ["sentence structure", "paragraph organization", "connecting ideas"],
                "exam_focus": "Writing clear sentences and short organized paragraphs",
            },
            {
                "id": "L4M4",
                "name": "Vocabulary Building",
                "description": "Expanding word knowledge through prefixes, suffixes, and context clues",
                "video_url": "https://www.youtube.com/watch?v=bSFAouFRKpg",
                "video_title": "Prefixes and Suffixes | Scratch Garden",
                "skills": ["prefixes", "suffixes", "context clues", "word meaning"],
                "exam_focus": "Understanding word meanings using word parts and context",
            },
        ],
    },
    5: {
        "name": "Level 5 - Mastery",
        "description": "Independent reading and self-monitoring",
        "modules": [
            {
                "id": "L5M1",
                "name": "Independent Reading",
                "description": "Reading grade-level text independently with confidence",
                "video_url": "https://www.youtube.com/watch?v=2oUb6PGdx5g",
                "video_title": "Reading Strategies | Crash Course",
                "skills": ["independent reading", "self-correction", "reading stamina"],
                "exam_focus": "Reading an age-appropriate passage independently and summarizing it",
            },
            {
                "id": "L5M2",
                "name": "Advanced Comprehension",
                "description": "Critical thinking, comparing texts, drawing conclusions",
                "video_url": "https://www.youtube.com/watch?v=WsOxBfkKNOA",
                "video_title": "Critical Reading | GCFGlobal",
                "skills": ["critical thinking", "text comparison", "drawing conclusions"],
                "exam_focus": "Analyzing text critically and forming supported opinions",
            },
            {
                "id": "L5M3",
                "name": "Creative Writing",
                "description": "Expressing ideas through structured creative writing",
                "video_url": "https://www.youtube.com/watch?v=LNoYrIe8YBo",
                "video_title": "Creative Writing for Kids | Scholastic",
                "skills": ["story structure", "descriptive writing", "creative expression"],
                "exam_focus": "Writing a short creative piece with clear structure",
            },
            {
                "id": "L5M4",
                "name": "Self-Monitoring Skills",
                "description": "Recognizing and fixing own mistakes while reading and writing",
                "video_url": "https://www.youtube.com/watch?v=PxD3tqLmufY",
                "video_title": "Self-Monitoring Reading | Teaching Channel",
                "skills": ["error detection", "self-correction", "metacognition"],
                "exam_focus": "Identifying and correcting errors in given text and own writing",
            },
        ],
    },
}


def get_level_modules(level: int) -> dict:
    """Get all module info for a given level."""
    return LEARNING_MODULES.get(level, LEARNING_MODULES[1])


def get_module(level: int, module_index: int) -> dict:
    """Get a specific module (0-indexed)."""
    level_data = get_level_modules(level)
    modules = level_data["modules"]
    if module_index < len(modules):
        return modules[module_index]
    return modules[0]


def get_total_modules(level: int) -> int:
    """Get number of modules in a level."""
    return len(LEARNING_MODULES.get(level, LEARNING_MODULES[1])["modules"])
