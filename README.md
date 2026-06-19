# autocontent-copilot

[Русский](#русский) · [English](#english)

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.3.0-informational.svg)](.claude-plugin/plugin.json)

---

## Русский

Контент-копилот для лидогенерации. Это бизнес-инструмент, а не SMM ради лайков: он двигает аудиторию по ступеням от «впервые услышал» до заявки и помогает на каждом шаге - разобрать бизнес, собрать план, написать и сверстать контент, опубликовать, замерить. Работает внутри вашего агента: Claude, Codex или Hermes.

### Что это

Открытый метод плюс коннектор к серверу генерации. В этом репозитории лежит сам метод: набор скиллов (markdown) и гайд, которые ставятся в вашего агента. Тяжёлая генерация - картинки, видео, карусели, озвучка, рендер - выполняется на нашем сервере по подключению. Локально ничего тяжёлого ставить не надо: ни Python, ни Node, ни рантайма. Плагин у вас - это только markdown-скиллы и настройка коннектора к удалённому MCP-серверу.

Метод правится здесь, в открытом репозитории, и обновляется у всех сразу.

### Установка

Под каждую морду своя команда. Можно просто сказать своему агенту: «поставь плагин из этого репозитория» - и он сделает всё сам.

Claude:

```
/plugin marketplace add Drtduck/content-factory
/plugin install autocontent-copilot@autocontent-marketplace
```

Codex:

```
codex plugin marketplace add Drtduck/content-factory
codex plugin add autocontent-copilot@autocontent-marketplace
```

Hermes (через скилл-тап, плагин у нас без Python - только markdown-скиллы):

```
hermes skills tap add Drtduck/content-factory
hermes skills install Drtduck/content-factory/skills/copilot
hermes skills install Drtduck/content-factory/skills/onboarding
hermes skills install Drtduck/content-factory/skills/visual
hermes skills install Drtduck/content-factory/skills/video-editor
```

Коннектор к серверу в Hermes настраивается отдельно: добавьте фрагмент из `mcp.config.yaml` в раздел `mcp_servers` вашего `config.yaml`.

### Подключение генерации

Чтобы генерировать через сервер, получите токен у Processorio (контакт: https://processorio.ru) и положите его в переменную окружения `AUTOCONTENT_MCP_TOKEN`. Конфиг плагина уже ссылается на эту переменную, в файлы токен вписывать не нужно и не стоит.

```
export AUTOCONTENT_MCP_TOKEN="ваш-токен"
```

Без токена метод работает как метод: планы, скоринг текста, структура, разбор бизнеса. Генерация (картинки, видео, карусели, озвучка) - платная и живёт за токеном на сервере.

### Обновление

Claude: маркетплейс обновляется автоматически, при необходимости вручную через `/plugin marketplace update`.

Codex: `codex plugin marketplace upgrade`.

Hermes: `hermes skills update` (подтянет новые версии установленных скиллов из тапа).

### Что открыто, что на сервере

Открыто (этот репозиторий): метод, скиллы, гайд, плагины под три морды. Их можно читать, форкать и менять.

На сервере: генерация с метерингом, рендер визуала и видео, общая база. Это закрытая часть за токеном.

Метод и сервер разъезжаются по версиям независимо: правка метода тут доезжает до всех клиентов через обновление плагина, а логика генерации меняется на сервере и подхватывается тем же коннектором.

### Лицензия

AGPL-3.0. Форкать и использовать можно. Если вы поднимаете сервис на этом коде (в том числе доступный по сети), изменения нужно открыть. Полный текст: [LICENSE](LICENSE).

---

## English

A content copilot for lead generation. This is a business tool, not SMM for the sake of likes: it moves an audience along the stages from "just heard of you" to a submitted request, and helps at every step - understand the business, build a plan, write and lay out content, publish, measure. It runs inside your agent: Claude, Codex, or Hermes.

### What it is

An open method plus a connector to a generation server. This repository holds the method itself: a set of skills (markdown) and a guide that install into your agent. Heavy generation - images, video, carousels, voiceover, rendering - runs on our server over the connection. You do not install anything heavy locally: no Python, no Node, no runtime. The plugin on your side is only markdown skills plus the configuration of a connector to a remote MCP server.

The method is edited here, in the open repository, and updates for everyone at once.

### Install

Each agent has its own command. You can also just tell your agent: "install the plugin from this repository" and it will do everything itself.

Claude:

```
/plugin marketplace add Drtduck/content-factory
/plugin install autocontent-copilot@autocontent-marketplace
```

Codex:

```
codex plugin marketplace add Drtduck/content-factory
codex plugin add autocontent-copilot@autocontent-marketplace
```

Hermes (via a skill tap, since our plugin ships no Python - markdown skills only):

```
hermes skills tap add Drtduck/content-factory
hermes skills install Drtduck/content-factory/skills/copilot
hermes skills install Drtduck/content-factory/skills/onboarding
hermes skills install Drtduck/content-factory/skills/visual
hermes skills install Drtduck/content-factory/skills/video-editor
```

The connector to the server is configured separately in Hermes: add the fragment from `mcp.config.yaml` into the `mcp_servers` section of your `config.yaml`.

### Connecting generation

To generate through the server, get a token from Processorio (contact: https://processorio.ru) and put it into the `AUTOCONTENT_MCP_TOKEN` environment variable. The plugin config already references this variable, so there is no need to hardcode the token anywhere.

```
export AUTOCONTENT_MCP_TOKEN="your-token"
```

Without a token the method still works as a method: plans, text scoring, structure, business analysis. Generation (images, video, carousels, voiceover) is paid and lives behind the token on the server.

Note for Codex: when configured through `config.toml`, Codex can read the token from the environment via `bearer_token_env_var` pointing to `AUTOCONTENT_MCP_TOKEN`, so the value stays out of config files.

### Updating

Claude: the marketplace updates automatically, or run `/plugin marketplace update` manually when needed.

Codex: `codex plugin marketplace upgrade`.

Hermes: `hermes skills update` (pulls newer versions of installed skills from the tap).

### What is open, what is on the server

Open (this repository): the method, the skills, the guide, the plugins for all three agents. You can read, fork, and change them.

On the server: metered generation, visual and video rendering, the shared database. This is the closed part behind the token.

The method and the server version independently: a method change here reaches every client through a plugin update, while generation logic changes on the server and is picked up by the same connector.

### License

AGPL-3.0. You may fork and use it. If you run a service on this code (including one reachable over a network), you must release your changes. Full text: [LICENSE](LICENSE).
