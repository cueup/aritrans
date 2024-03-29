import streamlit as st  # building web apps in python
from PIL import Image  # for opening image files
from datetime import date  # provides date & time functions
from gtts import gTTS, lang  # for text speech
from googletrans import Translator  # provides translation functions
import streamlit.components.v1 as components

# setting app's title, icon & layout
st.set_page_config(page_title="TypeAri Universal Translate", page_icon="/favicon.ico", layout="centered")


def get_key(val):
    """function to find the key of the given value in the dict object

    Args:
        val (str): value to find key

    Returns:
        key(str): key for the given value
    """
    for key, value in lang.tts_langs().items():
        if val == value:
            return key


def main():
    #this code below is the statcounter tracking code
    takip= """
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){
            c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        })(window, document, "clarity", "script", "h4vxoiilqp");
    </script>
    """
    components.html(takip,width=1, height=1)
    
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>

    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # instance of Translator()
    trans = Translator()

    # gets gtts supported languages as dict
    langs = lang.tts_langs()

    # display current date & header
    st.header("TypeAri Universal Translate")
    st.write(f"Date : {date.today()}")

    input_text = st.text_input("Enter text to translate")  # gets text to translate
    lang_choice = st.selectbox(
        "Language to translate: ", list(langs.values())
    )  # shows the supported languages list as selectbox options

    if st.button("Translate"):
        if input_text == "":
            # if the user input is empty
            st.write("Please Enter text to translate")

        else:
            detect_expander = st.expander("Detected Language", expanded=True)
            with detect_expander:
                detect = trans.detect([input_text])[
                    0
                ]  # detect the user given text language
                detect_text = f"Detected Language : {langs[detect.lang]}"
                st.success(detect_text)  # displays the detected language

                # convert the detected text to audio file
                detect_audio = gTTS(text=input_text, lang=detect.lang, slow=False)
                detect_audio.save("user_detect.mp3")
                audio_file = open("user_detect.mp3", "rb")
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/ogg", start_time=0)

            trans_expander = st.expander("Translated Text", expanded=True)
            with trans_expander:
                translation = trans.translate(
                    input_text, dest=get_key(lang_choice)
                )  # translates user given text to target language
                translation_text = f"Translated Text : {translation.text}"
                st.success(translation_text)  # displays the translated text

                # convert the translated text to audio file
                translated_audio = gTTS(
                    text=translation.text, lang=get_key(lang_choice), slow=False
                )
                translated_audio.save("user_trans.mp3")
                audio_file = open("user_trans.mp3", "rb")
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/ogg", start_time=0)

                # download button to download translated audio file
                with open("user_trans.mp3", "rb") as file:
                    st.download_button(
                        label="Download",
                        data=file,
                        file_name="trans.mp3",
                        mime="audio/ogg",
                    )


if __name__ == "__main__":
    main()  # calls the main() first