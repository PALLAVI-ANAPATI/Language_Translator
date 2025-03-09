from quart import Quart, render_template, request, jsonify
from googletrans import Translator, LANGUAGES

app = Quart(__name__)

language_codes = list(LANGUAGES.keys())
language_names = list(LANGUAGES.values())

@app.route('/')
async def index():
    return await render_template(
        'index.html',
        source_languages=zip(language_codes, language_names),
        target_languages=zip(language_codes, language_names),
    )

@app.route('/translate', methods=['POST'])
async def translate_text():
    text_to_translate = (await request.form).get('text')
    source_language = (await request.form).get('source_language')
    target_language = (await request.form).get('target_language')

    if not text_to_translate or not source_language or not target_language:
        return jsonify({'translation': 'Please provide valid input.'})

    translator = Translator()
    try:
        translation_result = await translator.translate(
            text_to_translate, src=source_language, dest=target_language
        )
        translation = translation_result.text
    except Exception as e:
        print(f"Translation error: {e}")
        translation = "Translation failed. Please try again later."

    return jsonify({'translation': translation})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=False)
