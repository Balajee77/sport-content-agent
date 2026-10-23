
import sys
import streamlit as st

from pathlib import Path

PROJECT_PATH = str(Path(__file__).resolve().parent)

if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)







from agent.batch_generator import generate_batch
from agent.single_generator import generate_one_item
from utils.history import clear_history
from utils.validators import clean_source_url


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="SportsPulse AI",
    page_icon="🏆",
    layout="wide"
)


# ==========================================
# API KEYS
# ==========================================

try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
except Exception:
    GEMINI_API_KEY = None
    TAVILY_API_KEY = None


# ==========================================
# SESSION STATE
# ==========================================

if "items" not in st.session_state:
    st.session_state["items"] = []

if "last_settings" not in st.session_state:
    st.session_state.last_settings = {}


# ==========================================
# HELPERS
# ==========================================

def get_surface_text(item, surface):
    """
    Adapt generated text for Instagram surface.
    """

    content_type = item.get("type", "")

    if content_type == "MCQ":
        base = item.get("question", "")
    elif content_type == "True/False":
        base = item.get("statement", "")
    elif content_type == "Poll":
        base = item.get("prompt", "")
    elif content_type == "Fill in the Blank":
        base = item.get("sentence", "")
    elif content_type == "Guess the Number":
        base = item.get("question", "")
    else:
        base = ""

    if surface == "Story":
        return f"Quick challenge 👀\n\n{base}"

    elif surface == "Feed":
        return (
            f"Think you know {item.get('sport', 'sports')}? 👇\n\n"
            f"{base}\n\n"
            f"Drop your answer in the comments!"
        )

    elif surface == "Reel Caption":
        return (
            f"Only real fans get this right 🔥\n\n"
            f"{base}\n\n"
            f"Your guess? 👇"
        )

    return base


def get_grounding_badge(item):
    """
    Display the actual grounding method used.
    """

    grounding = item.get("grounding_source")

    if item.get("type") == "Poll" or grounding == "Opinion":
        return "🟣 Opinion"

    if grounding == "Web Search":
        return "🟢 Web Search"

    if grounding == "ChromaDB":
        return "🔵 ChromaDB"

    return "⚪ Grounded"


def render_source(item):
    source_title = item.get("source_title")
    source_url = clean_source_url(item.get("source_url"))

    if item.get("type") == "Poll":
        st.caption("Opinion-based content — no factual answer required.")
        return

    if source_title:
        st.write(f"**Source:** {source_title}")

    if source_url:
        st.write(f"**URL:** {source_url}")


def render_item(item, index, surface):
    content_type = item.get("type")

    with st.container(border=True):

        col_a, col_b = st.columns([4, 1])

        with col_a:
            st.subheader(f"{index + 1}. {content_type}")

        with col_b:
            st.caption(get_grounding_badge(item))

        st.caption(
            f"{item.get('sport', '')} • "
            f"{item.get('difficulty', 'Opinion')}"
        )

        if content_type == "MCQ":

            st.markdown(f"### {item['question']}")

            letters = ["A", "B", "C", "D"]

            for letter, option in zip(
                letters,
                item["options"]
            ):
                st.write(f"**{letter}.** {option}")

            with st.expander("Show Answer"):
                st.success(
                    f"Correct Answer: {item['correct_answer']}"
                )
                st.write(item["explanation"])


        elif content_type == "True/False":

            st.markdown(f"### {item['statement']}")
            st.write("True / False")

            with st.expander("Show Answer"):
                answer = (
                    "True"
                    if item["correct_answer"]
                    else "False"
                )

                st.success(
                    f"Correct Answer: {answer}"
                )

                st.write(item["explanation"])


        elif content_type == "Poll":

            st.markdown(f"### {item['prompt']}")

            col1, col2 = st.columns(2)

            with col1:
                st.button(
                    item["options"][0],
                    key=f"poll_a_{index}",
                    use_container_width=True
                )

            with col2:
                st.button(
                    item["options"][1],
                    key=f"poll_b_{index}",
                    use_container_width=True
                )

            st.info(
                "Opinion-based poll — no correct answer."
            )


        elif content_type == "Fill in the Blank":

            st.markdown(f"### {item['sentence']}")

            letters = ["A", "B", "C", "D"]

            for letter, option in zip(
                letters,
                item["options"]
            ):
                st.write(f"**{letter}.** {option}")

            with st.expander("Show Answer"):
                st.success(
                    f"Correct Answer: {item['correct_answer']}"
                )

                st.write(item["explanation"])


        elif content_type == "Guess the Number":

            st.markdown(f"### {item['question']}")

            st.write("Make your guess 🔢")

            with st.expander("Reveal Answer"):
                st.success(
                    f"Target Number: {item['target_number']}"
                )

                st.write(
                    f"Accepted Range: ±{item['tolerance']}"
                )

                st.write(item["explanation"])


        st.divider()

        st.markdown("#### Instagram-ready version")

        instagram_text = get_surface_text(
            item,
            surface
        )

        st.code(
            instagram_text,
            language=None
        )

        render_source(item)

        if st.button(
            "🔄 Regenerate This Item",
            key=f"regen_{index}",
            use_container_width=True
        ):

            settings = st.session_state.last_settings

            with st.spinner(
                "Regenerating item..."
            ):

                new_item = generate_one_item(
                    gemini_api_key=GEMINI_API_KEY,
                    tavily_api_key=TAVILY_API_KEY,
                    sport=settings["sport"],
                    difficulty=settings["difficulty"],
                    content_type=content_type
                )

                st.session_state["items"][index] = (
                    new_item
                )

                st.rerun()


# ==========================================
# HEADER
# ==========================================

st.title("🏆 SportsPulse AI")

st.subheader(
    "AI-Powered Sports Engagement Content Agent"
)

st.caption(
    "Generate grounded, diverse and Instagram-ready "
    "sports quizzes, polls and engagement content."
)

st.divider()


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("Content Settings")

    sport = st.selectbox(
        "Sport",
        [
            "Cricket",
            "Football",
            "Tennis",
            "Badminton",
            "Basketball"
        ]
    )

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Easy",
            "Medium",
            "Hard"
        ]
    )

    selected_types = st.multiselect(
        "Content Types",
        [
            "MCQ",
            "True/False",
            "Poll",
            "Fill in the Blank",
            "Guess the Number"
        ],
        default=[
            "MCQ",
            "True/False",
            "Poll"
        ]
    )

    batch_size = st.selectbox(
        "Batch Size",
        [4, 5]
    )

    surface = st.selectbox(
        "Instagram Surface",
        [
            "Story",
            "Feed",
            "Reel Caption"
        ]
    )

    st.caption(
        "Factual content is grounded using "
        "web search and historical retrieval."
    )


# ==========================================
# API CHECK
# ==========================================

if not GEMINI_API_KEY or not TAVILY_API_KEY:

    st.error(
        "API keys are missing. Add GEMINI_API_KEY "
        "and TAVILY_API_KEY."
    )

    st.stop()


# ==========================================
# GENERATE BUTTON
# ==========================================

if st.button(
    "✨ Generate Content",
    type="primary",
    use_container_width=True
):

    if not selected_types:

        st.warning(
            "Select at least one content type."
        )

    else:

        with st.spinner(
            "Generating grounded sports content..."
        ):

            try:

                items = generate_batch(
                    gemini_api_key=GEMINI_API_KEY,
                    tavily_api_key=TAVILY_API_KEY,
                    sport=sport,
                    difficulty=difficulty,
                    selected_types=selected_types,
                    batch_size=batch_size
                )

                st.session_state["items"] = items

                st.session_state.last_settings = {
                    "sport": sport,
                    "difficulty": difficulty,
                    "selected_types": selected_types,
                    "batch_size": batch_size,
                    "surface": surface
                }

                st.success(
                    "Content generated successfully ✅"
                )

            except Exception as error:

                st.error(
                    "Generation failed."
                )

                st.exception(error)


# ==========================================
# DISPLAY ITEMS
# ==========================================

if st.session_state["items"]:

    st.divider()

    st.header("Generated Content")

    current_surface = st.session_state.last_settings.get(
        "surface",
        surface
    )

    for index, item in enumerate(
        st.session_state["items"]
    ):

        render_item(
            item,
            index,
            current_surface
        )


    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔄 Regenerate Full Batch",
            use_container_width=True
        ):

            settings = st.session_state.last_settings

            with st.spinner(
                "Regenerating full batch..."
            ):

                new_items = generate_batch(
                    gemini_api_key=GEMINI_API_KEY,
                    tavily_api_key=TAVILY_API_KEY,
                    sport=settings["sport"],
                    difficulty=settings["difficulty"],
                    selected_types=settings["selected_types"],
                    batch_size=settings["batch_size"]
                )

                st.session_state["items"] = new_items

                st.rerun()


    with col2:

        if st.button(
            "🧹 Clear Generated Content",
            use_container_width=True
        ):

            st.session_state["items"] = []

            st.rerun()
