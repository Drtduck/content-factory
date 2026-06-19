# onboarding

Навык морды для воронки первого запуска: пошагово доводит клиента от «только зашёл» до готового рабочего пространства. Семь шагов - приветствие и позиционирование (лидоген-копилот), проверка связи (`get_my_account` / `get_onboarding_checklist`), профиль компании (`set_client_profile` у оператора + `update_brand_facts` у клиента), фирстиль (`get_brand_identity`/`set_brand_identity`), ключи интеграций (`get_onboarding_checklist`, `submit_integration_key`, `set_integration_config`), лимит расходов (`set_client_spend_cap` OWNER-only, остаток клиент видит в `get_my_account`), финальная сверка (`get_onboarding_checklist` + `get_integration_status`) и передача копилоту.

Каталог интеграций: postmypost, image (fal/др.), video_analysis (Gemini), elevenlabs, yandex_speechkit, apify, carousel (локальный).

Ключи передаются write-only: значение принимается сервером и пишется в `{workspace}/secrets/.env`, но никогда не возвращается, не логируется и не сохраняется на стороне клиента. Шаги профиля и лимита - OWNER-only (оператор). См. `SKILL.md`.
