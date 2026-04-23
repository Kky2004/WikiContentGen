import streamlit as st
import wikipedia
from gtts import gTTS
from reportlab.pdfgen import canvas
import os

st.title("📚 Wikipedia Summary")

if "menu" not in st.session_state:
    st.session_state.menu = "main"
    st.session_state.results = []
    st.session_state.summary = ""

if st.session_state.menu == "main":
    st.write("=== Enter the choice ===")
    choice = st.radio("", ["StartSearch", "Exit"])

    if choice == "StartSearch":
        if st.button("Continue"):
            st.session_state.menu = "search"
            st.rerun()

    elif choice == "Exit":
        st.write("Program Ended")

elif st.session_state.menu == "search":
    query = st.text_input("Enter the keyword")

    if st.button("Search"):
        try:
            results = wikipedia.search(query)
            if results:
                st.session_state.results = results
                st.session_state.menu = "select"
                st.rerun()
            else:
                st.warning("No results found")
        except Exception as e:
            st.error(f"Exception is {e}")

elif st.session_state.menu == "select":
    st.write("### Select the options from here")

    for i, item in enumerate(st.session_state.results, start=1):
        st.write(f"{i} -- {item}")

    inp = st.number_input(
        "Enter the input you want to brief",
        min_value=1,
        max_value=len(st.session_state.results),
        step=1
    )

    if st.button("Confirm"):
        try:
            summary = wikipedia.summary(st.session_state.results[int(inp) - 1])
            st.session_state.summary = summary
            st.session_state.menu = "format"
            st.rerun()
        except Exception as e:
            st.error(f"Exception is {e}")

elif st.session_state.menu == "format":
    st.subheader("Summary")
    st.write(st.session_state.summary)

    fmt = st.radio("Enter the format you want", ["audio", "pdf"])
    filename = st.text_input("Enter the filename (without extension)")

    if st.button("Generate"):
        try:
            if not filename:
                st.warning("Enter the valid filename")
            else:
                summary = st.session_state.summary

                if fmt == "audio":
                    file_path = f"{filename}.mp3"
                    gTTS(text=summary).save(file_path)

                    with open(file_path, "rb") as f:
                        st.download_button("Download Audio", f, file_name=f"{filename}.mp3")

                    os.remove(file_path)
                    st.success("Your audio file is ready")

                elif fmt == "pdf":
                    file_path = f"{filename}.pdf"

                    c = canvas.Canvas(file_path)
                    text = c.beginText(100, 800)
                    text.setFont("Helvetica", 10)

                    words = summary.split()
                    line = ""

                    for word in words:
                        if len(line + word) < 90:
                            line += word + " "
                        else:
                            text.textLine(line)
                            line = word + " "

                    text.textLine(line)

                    c.drawText(text)
                    c.save()

                    with open(file_path, "rb") as f:
                        st.download_button("Download PDF", f, file_name=f"{filename}.pdf")

                    os.remove(file_path)
                    st.success("Your pdf file is ready")

        except Exception as e:
            st.error(f"Exception is {e}")

    if st.button("Back to Menu"):
        st.session_state.menu = "main"
        st.session_state.results = []
        st.session_state.summary = ""
        st.rerun()