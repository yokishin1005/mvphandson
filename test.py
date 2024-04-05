
from deepgram import DeepgramClient, PrerecordedOptions, FileSource
DG_API_KEY = "95051d87e12415baec2a103eb390ce012aa7779a"

import openai
openai.api_type = "azure"
openai.api_base = "https://tech0-gpt-event-westus.openai.azure.com"
openai.api_key = "200e3e4edb1941f9abe0ae005789ad33"
openai.api_version = "2023-05-15"

import streamlit as st
def transcribe_file(audio_bytes):
    try:
        deepgram = DeepgramClient(DG_API_KEY)
        payload: FileSource = {
            "buffer": audio_bytes,
        }

        options = PrerecordedOptions(
            model="nova-2",
            language="ja",
            smart_format=True,
            diarize=True,
        )

        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
        return response

    except Exception as e:
        print(f"Exception: {e}")
        return None

def summary(transcript):
    prompt = f"議事録を作成してください。今回の会議の目的と結論、会議の発言の要点をそれぞれ箇条書きでまとめてください。：\n{transcript}"

    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo",  # 適切なエンジン名を指定
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    summary_result = response.choices[0]["message"]["content"].strip()
    return summary_result

def main():
    st.title('オーディオファイルをアップロードしてください')

    with st.spinner('ファイルを読み込み中...'):
        uploaded_file = st.file_uploader("ファイルを選択してください", type=['mp4', 'wav', 'm4a'])

    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()

        with st.spinner('文字起こし中...'):
            response = transcribe_file(audio_bytes)

        if response is not None:
            transcription = response.to_dict()
            transcript_text = transcription["results"]["channels"][0]["alternatives"][0]["transcript"]
            st.write("文字起こし結果：")
            st.write(transcript_text)

            with st.spinner('議事録作成中...'):
                summarized_text = summary(transcript_text)
                st.write("議事録：")
                st.write(summarized_text)
        else:
            st.error('エラーが発生しました。')

if __name__ == "__main__":
    main()
