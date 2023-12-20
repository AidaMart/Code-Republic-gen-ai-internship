from easygoogletranslate import EasyGoogleTranslate

translator = EasyGoogleTranslate(
    source_language='en',
    target_language='hy',
    timeout=10
)
result = translator.translate('This is a wonderful film.')

print(result)
