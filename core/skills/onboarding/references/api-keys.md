# Где и как получить ключи интеграций

Справочник для шага «Ключи интеграций» онбординга. По каждому провайдеру: зачем он, какое значение нужно, и пошагово где его взять. Ссылки ведут на панели и документацию провайдеров. Клиент НЕ вставляет ключи в чат: он заполняет файл `КЛЮЧИ.env` в папке проекта (морда генерит шаблон, краткие версии этих инструкций кладёт в комментарии файла), морда читает файл локально, сохраняет значения через `submit_integration_key(...)`, проверяет через `verify_integration_key(...)` и удаляет файл. Сами ключи нигде не цитируются и в чат не попадают.

**Managed-режим:** анализ сайта, мониторинг соцсетей (сбор постов и референсов) и анализ референсных видео работают на стороне сервиса - но только если у сервиса заведены owner-ключи Apify и Gemini. Поэтому `APIFY_TOKEN` и `GEMINI_API_KEY` мы по умолчанию кладём в шаблон `КЛЮЧИ.env`: чтобы клиент мог дать свои токены и чтобы скрейп и анализ не умерли молча, если owner-ключа нет. Поля необязательные - не заполнит, останется managed-режим там, где он доступен. Свои ключи также обязательны для генерации картинок, озвучки и публикации.

Если у клиента что-то не получается с конкретным провайдером - можно отправить вопрос команде сервиса через `submit_feedback(text=..., kind=feedback)` или попросить оператора настроить ключ за него.

## PostMyPost (публикация и метрики)

Зачем: публикация постов в соцсети и сбор метрик охвата.
Интеграция: `postmypost`. Значение: `POSTMYPOST_TOKEN`.

Как получить:
1. Зайти в кабинет PostMyPost: https://postmypost.io (войти или зарегистрироваться).
2. Открыть Настройки аккаунта -> раздел API.
3. Создать новый API-токен и скопировать его.
4. Документация по API: https://postmypost.io/help (раздел про API и интеграции).

Дополнительно для реального режима копилоту нужен `endpoint_url` (адрес API, строго `https://...`) - его задаёт оператор или клиент через `set_integration_config(integration="postmypost", settings={"endpoint_url": "https://..."})`.

## fal (генерация картинок, провайдер по умолчанию)

Зачем: генерация картинок к постам. Провайдер по умолчанию для интеграции `image`.
Интеграция: `image`. Значение: `AUTOCONTENT_IMAGE_API_KEY`.

Как получить (fal):
1. Зайти на https://fal.ai и войти (можно через Google/GitHub).
2. Открыть раздел ключей: https://fal.ai/dashboard/keys
3. Нажать создать ключ (Add key / Create API key) и скопировать значение.
4. Документация: https://docs.fal.ai

Если клиент выбрал другого провайдера картинок (openai / ideogram / recraft), ключ берётся в кабинете соответствующего провайдера:
- OpenAI: https://platform.openai.com/api-keys
- Ideogram: https://ideogram.ai (раздел API / developer)
- Recraft: https://www.recraft.ai (раздел API)

Сначала зафиксируй выбор провайдера через `set_integration_config(integration="image", settings={"provider": <выбор>})`, потом собирай ключ. Картинки считаются подключёнными, только когда есть ключ и включён `enable_real`.

## Apify (сбор референсов конкурентов и отзывов)

Зачем: сбор контента конкурентов, постов из соцсетей и отзывов/сайтов как материал для плана и для tone of voice. Источники: instagram, tiktok, youtube, facebook, twitter, telegram, linkedin, website, google_maps_reviews.
По умолчанию `APIFY_TOKEN` кладётся в шаблон `КЛЮЧИ.env`. Managed-режим (на owner-токене сервиса) работает, только если owner-ключ заведён; свой токен клиента нужен, чтобы сбор не умер молча, когда owner-ключа нет. Поле необязательное.
Интеграция: `apify`. Значение: `APIFY_TOKEN`.

Как получить:
1. Зайти в консоль Apify: https://console.apify.com (войти или зарегистрироваться).
2. Открыть Settings -> Integrations (или сразу: https://console.apify.com/settings/integrations).
3. Скопировать Personal API token.
4. Документация: https://docs.apify.com/platform/integrations/api

## Google Gemini (анализ референсных видео)

Зачем: анализ референсных видео (Gemini нативно понимает видео).
По умолчанию `GEMINI_API_KEY` кладётся в шаблон `КЛЮЧИ.env`. Managed-режим (на owner-токене сервиса) работает, только если owner-ключ заведён; свой токен клиента нужен, чтобы анализ не умер молча, когда owner-ключа нет. Поле необязательное.
Интеграция: `video_analysis`. Значение: `GEMINI_API_KEY`.

Как получить:
1. Зайти в Google AI Studio: https://aistudio.google.com
2. Открыть страницу ключей: https://aistudio.google.com/apikey
3. Создать API-ключ (Create API key) и скопировать его.
4. Документация: https://ai.google.dev/gemini-api/docs

## ElevenLabs (основная озвучка, TTS)

Зачем: основная озвучка видео (text-to-speech).
Интеграция: `elevenlabs`. Значение: `ELEVENLABS_API_KEY`.

Как получить:
1. Зайти на https://elevenlabs.io и войти.
2. Открыть профиль -> раздел API Keys (или сразу: https://elevenlabs.io/app/settings/api-keys).
3. Создать ключ и скопировать значение.
4. Документация: https://elevenlabs.io/docs

## Yandex SpeechKit (резервная озвучка, fallback TTS)

Зачем: резервная озвучка, если основная недоступна.
Интеграция: `yandex_speechkit`. Нужны ДВА значения: `YANDEX_SPEECHKIT_API_KEY` и `YANDEX_FOLDER_ID`.

Как получить:
1. Зайти в консоль Yandex Cloud: https://console.cloud.yandex.ru
2. Создать сервисный аккаунт и выдать ему роль `ai.speechkit-tts.user`.
3. Для сервисного аккаунта создать API-ключ - это значение `YANDEX_SPEECHKIT_API_KEY`.
4. `YANDEX_FOLDER_ID` - идентификатор каталога, виден в консоли в свойствах каталога (адрес каталога вида `https://console.cloud.yandex.ru/folders/<folder_id>`).
5. Документация SpeechKit: https://yandex.cloud/ru/docs/speechkit
6. Про сервисные аккаунты и ключи: https://yandex.cloud/ru/docs/iam/operations/api-key/create

Оба значения сохраняются по отдельности через `submit_integration_key` (по разу на каждое имя), затем проверяются через `verify_integration_key("yandex_speechkit")`.

## Carousel (локальный генератор каруселей)

Ключ не нужен - это локальный движок (`local: true`). Включается флагом `enable_real` через `set_integration_config(integration="carousel", settings={"enable_real": true})`. В справочник по ключам попадает только для полноты картины.
